import contextlib
import hashlib
import os
import re
import tempfile
import stat
import zipfile

from base64 import urlsafe_b64encode
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

from poetry.__version__ import __version__
from poetry.semver.constraints import Constraint
from poetry.semver.constraints import MultiConstraint

from ..utils.helpers import normalize_file_permissions
from .builder import Builder


wheel_file_template = """\
Wheel-Version: 1.0
Generator: poetry {version}
Root-Is-Purelib: true
""".format(version=__version__)


class WheelBuilder(Builder):

    def __init__(self, poetry, io, target_fp):
        super().__init__(poetry, io)

        self._records = []

        # Open the zip file ready to write
        self._wheel_zip = zipfile.ZipFile(target_fp, 'w',
                                          compression=zipfile.ZIP_DEFLATED)

    @classmethod
    def make_in(cls, poetry, io, directory) -> SimpleNamespace:
        # We don't know the final filename until metadata is loaded, so write to
        # a temporary_file, and rename it afterwards.
        (fd, temp_path) = tempfile.mkstemp(suffix='.whl',
                                           dir=str(directory))
        try:
            with open(fd, 'w+b') as fp:
                wb = WheelBuilder(poetry, io, fp)
                wb.build()

            wheel_path = directory / wb.wheel_filename
            os.replace(temp_path, str(wheel_path))
        except:
            os.unlink(temp_path)
            raise

        return SimpleNamespace(builder=wb, file=wheel_path)

    @classmethod
    def make(cls, poetry, io) -> SimpleNamespace:
        """Build a wheel in the dist/ directory, and optionally upload it.
            """
        dist_dir = poetry.file.parent / 'dist'
        try:
            dist_dir.mkdir()
        except FileExistsError:
            pass

        return cls.make_in(poetry, io, dist_dir)

    def build(self) -> None:
        self._io.writeln(' - Building <info>wheel</info>')
        try:
            self.copy_module()
            self.write_metadata()
            self.write_record()
        finally:
            self._wheel_zip.close()

        self._io.writeln(f' - Built <comment>{self.wheel_filename}</>')

    def copy_module(self) -> None:
        if self._module.is_package():
            files = self.find_files_to_add()

            # Walk the files and compress them,
            # sorting everything so the order is stable.
            for file in sorted(files):
                full_path = self._path / file

                # Do not include topmost files
                if full_path.relative_to(self._path) == Path(file.name):
                    continue

                self._add_file(full_path, file)
        else:
            self._add_file(str(self._module.path), self._module.path.name)

    def write_metadata(self):
        if 'scripts' in self._poetry.config or 'plugins' in self._poetry.config:
            with self._write_to_zip(self.dist_info + '/entry_points.txt') as f:
                self._write_entry_points(f)

        for base in ('COPYING', 'LICENSE'):
            for path in sorted(self._path.glob(base + '*')):
                self._add_file(path, '%s/%s' % (self.dist_info, path.name))

        with self._write_to_zip(self.dist_info + '/WHEEL') as f:
            self._write_wheel_file(f)

        with self._write_to_zip(self.dist_info + '/METADATA') as f:
            self._write_metadata_file(f)

    def write_record(self):
        # Write a record of the files in the wheel
        with self._write_to_zip(self.dist_info + '/RECORD') as f:
            for path, hash, size in self._records:
                f.write('{},sha256={},{}\n'.format(path, hash, size))
            # RECORD itself is recorded with no hash or size
            f.write(self.dist_info + '/RECORD,,\n')

    @property
    def dist_info(self) -> str:
        return self.dist_info_name(self._package.name, self._package.version)

    @property
    def wheel_filename(self) -> str:
        tag = ('py2.' if self.supports_python2() else '') + 'py3-none-any'
        return '{}-{}-{}.whl'.format(
            re.sub("[^\w\d.]+", "_", self._package.pretty_name, flags=re.UNICODE),
            re.sub("[^\w\d.]+", "_", self._package.version, flags=re.UNICODE),
            tag)

    def supports_python2(self):
        return self._package.python_constraint.matches(
            MultiConstraint([
                Constraint('>=', '2.0.0'),
                Constraint('<', '3.0.0')
            ])
        )

    def dist_info_name(self, distribution, version) -> str:
        escaped_name = re.sub("[^\w\d.]+", "_", distribution, flags=re.UNICODE)
        escaped_version = re.sub("[^\w\d.]+", "_", version, flags=re.UNICODE)

        return '{}-{}.dist-info'.format(escaped_name, escaped_version)

    def _add_file(self, full_path, rel_path):
        full_path, rel_path = str(full_path), str(rel_path)
        if os.sep != '/':
            # We always want to have /-separated paths in the zip file and in
            # RECORD
            rel_path = rel_path.replace(os.sep, '/')

        zinfo = zipfile.ZipInfo.from_file(full_path, rel_path)

        # Normalize permission bits to either 755 (executable) or 644
        st_mode = os.stat(full_path).st_mode
        new_mode = normalize_file_permissions(st_mode)
        zinfo.external_attr = (new_mode & 0xFFFF) << 16  # Unix attributes

        if stat.S_ISDIR(st_mode):
            zinfo.external_attr |= 0x10  # MS-DOS directory flag

        hashsum = hashlib.sha256()
        with open(full_path, 'rb') as src, self._wheel_zip.open(zinfo,
                                                                'w') as dst:
            while True:
                buf = src.read(1024 * 8)
                if not buf:
                    break
                hashsum.update(buf)
                dst.write(buf)

        size = os.stat(full_path).st_size
        hash_digest = urlsafe_b64encode(hashsum.digest()).decode(
            'ascii').rstrip('=')

        self._records.append((rel_path, hash_digest, size))

    @contextlib.contextmanager
    def _write_to_zip(self, rel_path):
        sio = StringIO()
        yield sio

        # The default is a fixed timestamp rather than the current time, so
        # that building a wheel twice on the same computer can automatically
        # give you the exact same result.
        date_time = (2016, 1, 1, 0, 0, 0)
        zi = zipfile.ZipInfo(rel_path, date_time)
        b = sio.getvalue().encode('utf-8')
        hashsum = hashlib.sha256(b)
        hash_digest = urlsafe_b64encode(
            hashsum.digest()
        ).decode('ascii').rstrip('=')

        self._wheel_zip.writestr(zi, b, compress_type=zipfile.ZIP_DEFLATED)
        self._records.append((rel_path, hash_digest, len(b)))

    def _write_entry_points(self, fp):
        """
        Write entry_points.txt.
        """
        entry_points = self.convert_entry_points()

        for group_name in sorted(entry_points):
            fp.write('[{}]\n'.format(group_name))
            for ep in sorted(entry_points[group_name]):
                fp.write(ep.replace(' ', ''))

            fp.write('\n')

    def _write_wheel_file(self, fp):
        fp.write(wheel_file_template)

        if self.supports_python2():
            fp.write("Tag: py2-none-any\n")

        fp.write("Tag: py3-none-any\n")

    def _write_metadata_file(self, fp):
        """
        Write out metadata in the 1.x format (email like)
        """
        fp.write('Metadata-Version: 1.2\n')
        fp.write(f'Name: {self._package.name}\n')
        fp.write(f'Version: {self._package.version}\n')
        fp.write(f'Summary: {self._package.description}\n')
        fp.write(f'Home-page: {self._package.homepage or self._package.repository_url or "UNKNOWN"}\n')
        fp.write(f'License: {self._package.license or "UNKOWN"}\n')

        # Optional fields
        if self._package.keywords:
            fp.write(f"Keywords: {','.join(self._package.keywords)}\n")

        if self._package.authors:
            author = self.convert_author(self._package.authors[0])

            fp.write(f'Author: {author["name"]}\n')
            fp.write(f'Author-email: {author["email"]}\n')

        if self._package.python_versions != '*':
            constraint = self._package.python_constraint
            if isinstance(constraint, MultiConstraint):
                python_requires = ','.join(
                    [str(c).replace(' ', '') for c in constraint.constraints]
                )
            else:
                python_requires = str(constraint).replace(' ', '')

            fp.write(f'Requires-Python: {python_requires}\n')

        classifiers = self.get_classifers()
        for classifier in classifiers:
            fp.write(f'Classifier: {classifier}\n')

        for dep in self._package.requires:
            fp.write('Requires-Dist: {}\n'.format(dep.to_pep_508()))

        if self._package.readme is not None:
            fp.write('\n' + self._package.readme + '\n')
