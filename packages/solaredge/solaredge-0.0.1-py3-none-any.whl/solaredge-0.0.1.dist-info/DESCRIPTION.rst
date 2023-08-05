# Solaredge
API wrapper for Solaredge monitoring service.

See https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf

## Create a new connection by supplying your Solaredge API key
```
s = solaredge.Solaredge("APIKEY")
```

## API Requests
12 API requests are supported. The methods return the parsed JSON response as a dict.

```
def get_list(self, size=100, start_index=0, search_text="", sort_property="", sort_order='ASC', status='Active,Pending'):

def get_details(self, site_id):

def get_data_period(self, site_id, parsed=False):

def get_energy(self, site_id, start_date, end_date, time_unit='DAY'):

def get_time_frame_energy(self, site_id, start_date, end_date, time_unit='DAY'):

def get_power(self, site_id, start_time, end_time):

def get_overview(self, site_id):

def get_power_details(self, site_id, start_time, end_time, meters=None):

def get_energy_details(self, site_id, start_time, end_time, meters=None, time_unit="DAY", as_dataframe=False):

def get_current_power_flow(self, site_id):

def get_storage_data(self, site_id, start_time, end_time, serials=None):

def get_inventory(self, site_id):
```

`get_energy_details` can also return the result as a Pandas DataFrame

## TODO
* Add support for bulk requests
* Add API documentation


