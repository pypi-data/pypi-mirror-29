"""
A module to interact with the Galaxy NgLims API.

Usage:
    In [1]: import bioblend.galaxy as bg

    In [2]: gi = bg.GalaxyInstance("http://localhost:8080", key="tttttttttttttttttttttttttttttttt")

    In [3]: import nglimsclient

    In [4]: nglimsclient.setup(gi)

    In [5]: gi.nglims.flowcell_details("C291VACXX")
    Out[5]:
    {'flowcell_id': 'C291VACXX',
     'lanes': [{'lane': 1,
       'slots': [{'analysis': 'Minimal',
         'recipe': 'Whole genome',
         'reference_genome': 'hg19',
         'sample_label': 'ROa23'}]},
      {'lane': 2,
       'slots': [{'analysis': 'Minimal',
         'recipe': 'Whole genome',
         'reference_genome': 'hg19',
         'sample_label': 'ROa24'}]},
...and so on
"""
from bioblend.galaxy.client import Client
from bioblend.galaxy.objects.client import ObjClient

import StringIO
import os


def setup(galaxy_instance):
    """
    Instantiate the client for the NgLims API and attach it to the
    GalaxyInstance at the `galaxy_instance.nglims` attribute.

    Returns:
        `galaxy_instance`, with a new attribute `nglims`
    """
    galaxy_instance.nglims = NglimsClient(galaxy_instance)
    return galaxy_instance


def setupObj(galaxy_instance):
    galaxy_instance.nglims = NglimsObjClient(galaxy_instance)
    return galaxy_instance


class NglimsClient(Client):
    def __init__(self, galaxy_instance):
        self.module = 'nglims'
        super(NglimsClient, self).__init__(galaxy_instance)
        # reset the client URL because the nglims API is at a non-standard location
        self.url = '/'.join([self.gi.base_url, self.module])

    def _make_nglims_url(self, service):
        return '/'.join([self.url, service])

    def flowcell_complete_details(self, flowcell_id):
        """
        Query the Galaxy instance for details for the given flowcell.
        """
        api_service = 'api_flowcell_complete_details'
        url = self._make_nglims_url(api_service)
        data = self.gi.make_post_request(url, {'run': flowcell_id})

        if 'error' in data:
            if data['error'].lower().startswith('did not find sequencing run'):
                # Special case:  the id isn't found
                return None
            else:
                raise RuntimeError("Error querying server: %s" % data['error'])
        else:
            return data

    def flowcell_details(self, flowcell_id):
        """
        Query the Galaxy instance for details for the given flowcell.

        Returns a dictionary containing details for the given flowcell.
        The dictionary will have the following keys:
        'flowcell_id' : ID of the selected flowcell (same value as
                        flowcell_id input parameter)
        'lanes' : a dictionary containing lanes definition
        Each lane is a dictionary with the following keys:
        'lane' : number of the lane
        'slots' : a list of slots definitions
        Each slot is a dictionary with the following keys:
        'sample_label' : label of the sample in this slot
        'reference_genome' : reference genome of the sample
        'analysis' : type of the analysis that will be performed on
                     this sample
        'barcode' : barcode of the sample in the selected lane (this
                    field can be missing if no barcode was specified
                    during the flowcell preparation step)
        """
        data = self.flowcell_complete_details(flowcell_id)

        if data is None:
            return None

        try:
            flowcell_details = dict(flowcell_id=str(data['run_name']),
                                    lanes=[])
            lanes = {}
            for x in data['details']:
                slot = dict(sample_label=str(x['name']),
                            reference_genome=str(x['genome_build']),
                            analysis=str(x['analysis']),
                            recipe=str(x['recipe']))

                if 'barcode' in x:
                    slot['barcode'] = str(x['barcode']['sequence'])
                lanes.setdefault(int(x['lane']), []).append(slot)

            for lane, slots in lanes.iteritems():
                flowcell_details['lanes'].append({'lane': lane, 'slots': slots})

            return flowcell_details

        except KeyError as e:
            # raise a RuntimeError.  If the response contains an 'error' message, we'll
            # use it to make the exception message.  Otherwise we'll recycle the text
            # from the KeyError (which should be the missing key).
            raise RuntimeError("Compatibility problem.  We didn't find all the expected " +
                               "fields in Galaxy's response.  Missing key: %s" % str(e))

    def flowcell_samplesheet(self, flowcell_id, lineterminator='\n', out_format='samplesheet', export_mode='FTP',
                             export_details=None, export_contact=None):
        """
        Download the details of a sequencing run as a CSV file.

        Returns a string containing a propertly formatted sample sheet.
        Returns None if the flowcell_id is unknown.

        Raises a RuntimeError in the case of other problems.
        """
        data = self.flowcell_complete_details(flowcell_id)

        if data is None:
            return None

        out_info = StringIO.StringIO()

        try:
            self.__format_sample_sheet(out_info, data, lineterminator, out_format, export_mode, export_details,
                                       export_contact)
            return out_info.getvalue()
        except KeyError as e:
            # raise a RuntimeError.  If the response contains an 'error' message, we'll
            # use it to make the exception message.  Otherwise we'll recycle the text
            # from the KeyError (which should be the missing key).
            raise RuntimeError("Compatibility problem.  We didn't find all the expected " +
                               "fields in Galaxy's response.  Missing key: %s" % str(e))

    def sample_detail_from_custom_name(self, sample_name):
        """
        Query the Galaxy instance for details for the given sample (by custom name).
        """
        api_service = 'api_get_sample_info'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, {'sample_name': sample_name})

    def get_list_flowcell(self):
        """
        Query get all flowcellids in nglims
        """
        api_service = 'api_get_list_flowcell'
        url = self._make_nglims_url(api_service)
        r = self.gi.make_get_request(url)
        if r.raise_for_status():
            raise RuntimeError("Error fetching data from Galaxy: %s" % str(r))

        data = r.json()
        return data

    def exists_flowcell_id(self, flowcell_id):
        """
        Check if exists run with flowcell_id
        """
        api_service = 'api_exists_flowcell_id'
        url = self._make_nglims_url(api_service)

        return self.gi.make_post_request(url, dict(fcid=flowcell_id))

    def run_details(self, flowcell_id):
        """
        Check if exists run with flowcell_id
        """
        api_service = 'api_run_details'
        url = self._make_nglims_url(api_service)

        return self.gi.make_post_request(url, dict(run=flowcell_id))

    def exists_sample_id(self, sample_id):
        """
        Check if exists sample with sample_id
        """
        api_service = 'api_exists_sample_id'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, dict(sample_id=sample_id))

    def exists_sample_in_run(self, sample_id, flowcell_id):
        """
        Check if exists sample with sample_id
        """
        api_service = 'api_exists_sample_in_run'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, dict(sample_id=sample_id, flowcell_id=flowcell_id))

    def get_api_key(self, user_email):
        """
        Get the apy_key for user with email 'user_mail'
        """
        api_service = 'api_get_api_key'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, dict(user_email=user_email))

    def get_nglims_config(self):
        """
        Get nglims configuration file: nglims.yaml (in json format)
        """
        api_service = 'api_get_nglims_config'
        url = self._make_nglims_url(api_service)
        r = self.gi.make_get_request(url)
        if r.raise_for_status():
            raise RuntimeError("Error fetching data from Galaxy: %s" % str(r))

        data = r.json()
        return data

    def delete_sample(self, sample_id):
        """
        Delete sample
        """
        api_service = 'api_delete_sample'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, dict(sample_id=sample_id))

    def get_new_sample_name(self):
        """
        Get a new sample name
        """
        api_service = 'api_get_new_sample_name'
        url = self._make_nglims_url(api_service)
        r = self.gi.make_get_request(url)
        if r.raise_for_status():
            raise RuntimeError("Error fetching data from Galaxy: %s" % str(r))

        data = r.json()
        return data

    def save_sample(self, sample_values):
        """
        Save sample
        """
        api_service = 'api_save_sample'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, sample_values)

    def samples_to_project(self, form_samples_to_project):
        """
        Associates samples to a project
        """
        api_service = 'api_samples_to_project'
        url = self._make_nglims_url(api_service)
        success, messages = self.gi.make_post_request(url, form_samples_to_project)
        return success, messages

    def move_samples_to_next_queue(self, ids):
        """
        Move samples to next queue
        """
        api_service = 'api_move_samples_to_next_queue'
        url = self._make_nglims_url(api_service)
        rsp = self.gi.make_post_request(url, ids)
        return rsp

    def add_samples_to_sequencing_run(self, form_flowcell):
        """
        Add_samples_to_sequencing_run: build flowcell
        """
        api_service = 'api_add_samples_to_sequencing_run'
        url = self._make_nglims_url(api_service)
        self.gi.make_post_request(url, form_flowcell)

    def confirm_import_samplesheet(self, data):
        """
        Confirm import samplesheet
        """
        api_service = 'api_confirm_import_samplesheet'
        url = self._make_nglims_url(api_service)
        rsp = self.gi.make_post_request(url, data)
        return rsp

    def save_export_request(self, export_request):
        """
        Save export sequencing data request
        """
        api_service = 'api_save_export_request'
        url = self._make_nglims_url(api_service)
        successfull, rsp = self.gi.make_post_request(url, export_request)
        return successfull, rsp

    def get_export_request(self, rid):
        """
        Get details of a sequencing data export request(s)
        by export request id
        """
        api_service = 'api_get_export_request'
        url = self._make_nglims_url(api_service)
        rsp = self.gi.make_post_request(url, {'rid': rid})
        return rsp

    def save_fc_status_report(self, status_report):
        """
        Save flowcell status report
        """
        api_service = 'api_save_fc_status_report'
        url = self._make_nglims_url(api_service)
        successfull, rsp = self.gi.make_post_request(url, status_report)
        return successfull, rsp

    def save_fastqc_report(self, fastqc_report):
        """
        Save fastqc report
        """
        api_service = 'api_save_fastqc_report'
        url = self._make_nglims_url(api_service)
        successfull, rsp = self.gi.make_post_request(url, fastqc_report)
        return successfull, rsp

    def get_export_request_by_status(self, status):
        """
        Query export request with status = status
        """
        api_service = 'api_get_export_request_by_status'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, {'status': status})

    def update_export_request_status(self, rid, status):
        """ Updatde export request state
            NEW RUNNING PAUSE FAILED SUCCESSFUL
        """
        api_service = 'api_update_export_request_state'
        url = self._make_nglims_url(api_service)
        return self.gi.make_post_request(url, dict(status=status, rid=rid))

    def send_mail(self, receivers=[], body='', subject=''):
        """
        Send email from nglims server
        """
        api_service = 'api_send_mail'
        url = self._make_nglims_url(api_service)
        if not isinstance(receivers, list):
            receivers = receivers.split(',')
        rsp = self.gi.make_post_request(url, dict(receivers=receivers, body=body, subject=subject))
        return rsp

    def update_sample_form_field(self, params):
        """
        Update sample form field
        """
        api_service = 'api_update_sample_form_field'
        url = self._make_nglims_url(api_service)
        successfull, rsp = self.gi.make_post_request(url, params)
        return successfull, rsp

    def update_sample_adapter(self, sample_id, adapter):
        """
        Update sample adapter
        """
        if self.exists_sample_id(sample_id):
            params = dict(sample_id=sample_id,
                          request_type_name='Library construction inputs',
                          update_fields={'adapters': adapter})

            return self.update_sample_form_field(params)

        msg = ['sample %s doesn\'t exist' % sample_id]
        return False, msg

    def update_sample_custom_name(self, sample_id, custom_name):
        """
        Update sample custom name
        """
        if self.exists_sample_id(sample_id):
            params = dict(sample_id=sample_id,
                          request_type_name='Sample values',
                          update_fields={'description': custom_name})

            return self.update_sample_form_field(params)

        msg = ['sample %s doesn\'t exist' % sample_id]
        return False, msg

    def update_sample_barcode_sequence(self, sample_id, barcode_sequence):
        """
        Update sample barcode sequence
        """
        if self.exists_sample_id(sample_id):
            params = dict(sample_id=sample_id,
                          request_type_name='Barcode details',
                          update_fields={'sequence': barcode_sequence})

            return self.update_sample_form_field(params)

        msg = ['sample %s doesn\'t exist' % sample_id]
        return False, msg

    def update_sample_recipe(self, sample_id, recipe):
        """
        Update sample recipe
        """
        if self.exists_sample_id(sample_id):
            params = dict(sample_id=sample_id,
                          request_type_name='Next gen sequencing inputs',
                          update_fields={'recipe': recipe})

            return self.update_sample_form_field(params)

        msg = ['sample %s doesn\'t exist' % sample_id]
        return False, msg

    @staticmethod
    def __format_sample_sheet(io, data, lineterminator='\n', out_format='samplesheet', export_mode='FTP',
                              export_details=None, export_contact=None):
        if lineterminator is None:
            raise ValueError("lineterminator can't be None")

        def write_line(row):
            io.write(','.join(map(str, row)))
            io.write(lineterminator)

        if out_format in ['samplesheet']:
            write_line(("FCID", "Lane", "SampleID", "SampleRef", "Index",
                        "Description", "Control", "Recipe", "Operator", "SampleProject", "CustomerSampleID"))
            flowcell_id = data['run_name']
            for x in data['details']:
                sample_id = x['name']
                if str(x['description']) == "control" and str(x['genome_build']) == "phix":
                    control = "Y"
                    recipe = 'control'
                    researcher = 'control'
                    project_name = 'control'
                else:
                    control = "N"
                    recipe = x['recipe']
                    researcher = x['researcher']
                    project_name = x['project_name']
                    description = ''
                    customer_sample_id = x['description']

                if 'multiplex' in x:
                    for mt in x['multiplex']:
                        barcode = mt['sequence']
                        write_line((flowcell_id, x['lane'], sample_id,
                                    x['genome_build'], barcode, description,
                                    control, recipe, researcher, project_name,
                                    customer_sample_id))
                else:
                    barcode = ''
                    write_line((flowcell_id, x['lane'], sample_id,
                                x['genome_build'], barcode, description,
                                control, recipe, researcher, project_name,
                                customer_sample_id))

        elif out_format in ['export_request']:
            write_line((
                "FCID", "SampleID", "CustomerSampleID", "SampleProject", "ExportMode", "ExportDetails", "ExportContact",
                "ExportDescription"))
            flowcell_id = data['run_name']
            samples = []
            for x in data['details']:
                sample_id = x['name']

                if sample_id not in samples:
                    samples.append(sample_id)
                    project_name = x['project_name']
                    customer_sample_id = x['description']
                    export_description = "%s - %s" % (flowcell_id, project_name)
                    write_line((flowcell_id, sample_id, customer_sample_id, project_name, export_mode, export_details,
                                export_contact, export_description))

    def export_flowcell_samplesheet_to_local_path(self, flowcell_id, file_local_path, use_default_filename=True):
        """
        Exports a workflow in json format to a given local path.
        """
        flowcell_samplesheet_csv = self.flowcell_samplesheet(flowcell_id)
        if flowcell_samplesheet_csv is None:
            raise RuntimeError("Couldn't find flowcell with id %s" % flowcell_id)

        if use_default_filename:
            filename = 'samplesheet-%s.csv' % flowcell_id
            file_local_path = os.path.join(file_local_path, filename)

        with open(file_local_path, 'wb') as out_file:
            out_file.write(flowcell_samplesheet_csv)


class NglimsObjClient(ObjClient, NglimsClient):
    def __init__(self, galaxy_instance):
        self.module = 'nglims'
        super(NglimsObjClient, self).__init__(galaxy_instance)
        # reset the client URL because the nglims API is at a non-standard location
        self.url = '/'.join([self.gi.base_url, self.module])

# vim: expandtab tabstop=4 shiftwidth=4 autoindent
