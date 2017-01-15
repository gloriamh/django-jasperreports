import mimetypes
import os
import subprocess
import tempfile
import urllib

from django.conf import settings
from django.views.generic.base import View
from django.http import HttpResponse

BASE_DIR = os.path.dirname(__file__)
JASPERSTARTER_DIR = os.path.join(BASE_DIR, 'jasperstarter')

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()

def content_disposition_encode(request, filename):
    # See http://greenbytes.de/tech/tc2231/#attwithfn2231utf8
    if not isinstance(filename, unicode):
        filename = filename.decode('utf8')
    quoted = urllib.quote(filename.encode('utf8'))

    # TODO: remove line
    return 'attachment; filename*=utf-8\'\'%s' % quoted

    if u'MSIE' in request.META.get('HTTP_USER_AGENT', ''):
        return 'attachment; filename="%s"' % quoted
    else:
        return 'attachment; filename*=utf-8\'\'%s' % quoted

def HttpDownloadResponse(request, content, filename):
    resp = HttpResponse(content,
                        content_type=mimetypes.guess_type(filename)[0])
    resp['content-disposition'] = (
        content_disposition_encode(request, filename))
    return resp

class PDFReportView(View):
    report_name = None
    pdf_name = None
    report_parameters = {}
    additional_parms = []

    def report_parameters_args(self):
        return ['{0}={1}'.format(k, v)
                for (k, v) in self.report_parameters.items()]

    def get(self, request, *args, **kwargs):
        with tempfile.NamedTemporaryFile() as output_file:
            args = [os.path.join(JASPERSTARTER_DIR, 'bin/jasperstarter'),
                    'pr', os.path.join(
                        settings.JASPERREPORTS_DIR, self.report_name),
                    '-f', 'pdf',
                    '-o', output_file.name,
                    '--jdbc-dir', os.path.join(JASPERSTARTER_DIR, 'jdbc/'),
                    '-t', 'mysql',
                    '-u', settings.DATABASES['default']['USER'],
                    '-p', settings.DATABASES['default']['PASSWORD'], 
                    '-H', settings.DATABASES['default']['HOST'],
                    '-n', settings.DATABASES['default']['NAME']]
            if self.report_parameters:
                args += ['-P'] + self.report_parameters_args()
            args += self.additional_parms
            subprocess.check_call(args)
            pdf = read_file('{}.pdf'.format(output_file.name))

        return HttpDownloadResponse(request, pdf, self.pdf_name)
