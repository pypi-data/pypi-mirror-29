# This file is part of Checkbox.
#
# Copyright 2016 Canonical Ltd.
# Written by:
#   Sylvain Pineau <sylvain.pineau@canonical.com>
#
# Checkbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.

#
# Checkbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Checkbox.  If not, see <http://www.gnu.org/licenses/>.

"""
:mod:`plainbox.impl.exporter.tar` -- Tar exporter
=================================================

.. warning::
    THIS MODULE DOES NOT HAVE STABLE PUBLIC API
"""

import io
import os
import tarfile
import time

from plainbox.impl.exporter import SessionStateExporterBase
from plainbox.impl.exporter.jinja2 import Jinja2SessionStateExporter
from plainbox.impl.exporter.xlsx import XLSXSessionStateExporter
from plainbox.impl.providers import get_providers
from plainbox.impl.unit.exporter import ExporterUnitSupport


class TARSessionStateExporter(SessionStateExporterBase):
    """Session state exporter creating Tar archives."""

    SUPPORTED_OPTION_LIST = ()

    def dump_from_session_manager(self, manager, stream):
        """
        Extract data from session manager and dump it into the stream.

        :param session_manager:
            SessionManager instance that manages session to be exported by
            this exporter
        :param stream:
            Byte stream to write to.

        """
        html_stream = io.BytesIO()
        options_list = [
            SessionStateExporterBase.OPTION_WITH_COMMENTS,
            SessionStateExporterBase.OPTION_WITH_IO_LOG,
            SessionStateExporterBase.OPTION_FLATTEN_IO_LOG,
            SessionStateExporterBase.OPTION_WITH_JOB_DEFS,
            SessionStateExporterBase.OPTION_WITH_RESOURCE_MAP,
            SessionStateExporterBase.OPTION_WITH_CATEGORY_MAP,
            SessionStateExporterBase.OPTION_WITH_CERTIFICATION_STATUS
        ]
        exporter_unit = self._get_all_exporter_units()[
            'com.canonical.plainbox::html']
        html_exporter = Jinja2SessionStateExporter(exporter_unit=exporter_unit)
        html_exporter.dump_from_session_manager(manager, html_stream)
        html_tarinfo = tarfile.TarInfo(name="submission.html")
        html_tarinfo.size = html_stream.tell()
        html_tarinfo.mtime = time.time()
        html_stream.seek(0)  # Need to rewind the file, puagh

        json_stream = io.BytesIO()
        options_list = [
            SessionStateExporterBase.OPTION_WITH_COMMENTS,
            SessionStateExporterBase.OPTION_WITH_IO_LOG,
            SessionStateExporterBase.OPTION_FLATTEN_IO_LOG,
            SessionStateExporterBase.OPTION_WITH_JOB_DEFS,
            SessionStateExporterBase.OPTION_WITH_RESOURCE_MAP,
            SessionStateExporterBase.OPTION_WITH_CATEGORY_MAP,
            SessionStateExporterBase.OPTION_WITH_CERTIFICATION_STATUS
        ]
        exporter_unit = self._get_all_exporter_units()[
            'com.canonical.plainbox::json']
        json_exporter = Jinja2SessionStateExporter(exporter_unit=exporter_unit)
        json_exporter.dump_from_session_manager(manager, json_stream)
        json_tarinfo = tarfile.TarInfo(name="submission.json")
        json_tarinfo.size = json_stream.tell()
        json_tarinfo.mtime = time.time()
        json_stream.seek(0)  # Need to rewind the file, puagh

        xlsx_stream = io.BytesIO()
        options_list = [
            XLSXSessionStateExporter.OPTION_WITH_SYSTEM_INFO,
            XLSXSessionStateExporter.OPTION_WITH_SUMMARY,
            XLSXSessionStateExporter.OPTION_WITH_DESCRIPTION,
            XLSXSessionStateExporter.OPTION_WITH_TEXT_ATTACHMENTS,
        ]
        xlsx_exporter = XLSXSessionStateExporter(options_list)
        xlsx_exporter.dump_from_session_manager(manager, xlsx_stream)
        xlsx_tarinfo = tarfile.TarInfo(name="submission.xlsx")
        xlsx_tarinfo.size = xlsx_stream.tell()
        xlsx_tarinfo.mtime = time.time()
        xlsx_stream.seek(0)  # Need to rewind the file, puagh

        job_state_map = manager.default_device_context.state.job_state_map
        with tarfile.TarFile.open(None, 'w|xz', stream) as tar:
            tar.addfile(html_tarinfo, html_stream)
            tar.addfile(json_tarinfo, json_stream)
            tar.addfile(xlsx_tarinfo, xlsx_stream)
            for job_id in manager.default_device_context.state.job_state_map:
                job_state = job_state_map[job_id]
                try:
                    recordname = job_state.result.io_log_filename
                except AttributeError:
                    continue
                for stdstream in ('stdout', 'stderr'):
                    filename = recordname.replace('record.gz', stdstream)
                    folder = 'test_output'
                    if job_state.job.plugin == 'attachment':
                        folder = 'attachment_files'
                    if os.path.exists(filename) and os.path.getsize(filename):
                        arcname = os.path.basename(filename)
                        if stdstream == 'stdout':
                            arcname = os.path.splitext(arcname)[0]
                        tar.add(filename, os.path.join(folder, arcname),
                                recursive=False)

    def dump(self, session, stream):
        pass

    def _get_all_exporter_units(self):
        exporter_map = {}
        for provider in get_providers():
            for unit in provider.unit_list:
                if unit.Meta.name == 'exporter':
                    exporter_map[unit.id] = ExporterUnitSupport(unit)
        return exporter_map
