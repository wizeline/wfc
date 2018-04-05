import os
import tempfile


class TmpIOHandler:
    def _open_tmpfile(self, mode):
        if not hasattr(self, '_tmp_path'):
            _, self._tmp_path = tempfile.mkstemp()

        self._tmp_file = open(self._tmp_path, mode)
        return self._tmp_file

    def _unlink_tmp_file(self):
        os.unlink(self._tmp_path)

    def close_tmpio(self):
        if hasattr(self, '_tmp_file'):
            self._tmp_file.close()

    def open_tmpin(self):
        return self._open_tmpfile('r')

    def open_tmpout(self):
        return self._open_tmpfile('w')

    def unlink_tmpio(self):
        if hasattr(self, '_tmp_file'):
            if not self._tmp_file.closed:
                self._tmp_file.close()
            self._unlink_tmp_file()
