@load base/protocols/http
@load icsnpp/s7comm

redef mmdb_dir = "GeoLite2DB";
redef Reporter::warnings_to_stderr = F;

module Scan;

export {

    redef enum Log::ID += { LOG };

    type Info: record {
        ts: time        &log;
        id: conn_id     &log;
        uid: string     &log;
        service: string &log &optional;
        history: string &log &optional;
    };
}

redef record connection += {
    scan: Info &optional;
};

export {
	const http_post_body_length = 200 &redef;
    const http_get_body_length = 200 &redef;

    type GeoInfo: record {
		country_code: string &optional &log;
		region: string &optional &log;
		city: string &optional &log;
		#latitude: double &optional &log;
		#longitude: double &optional &log;
        point: vector of double &optional &log;
	};

	type GeoPair: record {
		orig: GeoInfo &optional &log;
		resp: GeoInfo &optional &log;
	};	
}

redef record Conn::Info += {
		geo: GeoPair &optional &log;
	};

redef record HTTP::Info += {
	post_body: string &log &optional;
    #get_body: string &log &optional;
};

event log_post_bodies(f: fa_file, data: string)
	{
	for ( cid in f$conns )
		{
		local c: connection = f$conns[cid];
		if ( ! c$http?$post_body )
			c$http$post_body = "";

		if ( |c$http$post_body| > http_post_body_length )
			return;

		c$http$post_body = c$http$post_body + data;
		if ( |c$http$post_body| > http_post_body_length )
			{
			c$http$post_body = c$http$post_body[0:http_post_body_length] + "...";
			#Files::remove_analyzer(f, Files::ANALYZER_DATA_EVENT, [$stream_event=log_post_bodies]);
			}
		}
	}

event file_over_new_connection(f: fa_file, c: connection, is_orig: bool)
	{
	if ( is_orig && c?$http && c$http?$method && c$http$method == "POST" )
		{
		Files::add_analyzer(f, Files::ANALYZER_DATA_EVENT, [$stream_event=log_post_bodies]);
		}
	}


event connection_state_remove(c: connection) 
	{

    #Analisi connessioni per scan NMAP
    if (c$history == "ShAR" || c$history=="ShADadfR" || c$history=="ShR"){
        local rec: Scan::Info = [$ts=network_time(), $id=c$id, $history=c$history, $uid = c$uid];
        c$scan = rec;
        Log::write(Scan::LOG, rec);
        }

    #GeoIP Lookup

	local orig_geo: GeoInfo;
	local orig_loc = lookup_location(c$id$orig_h);    
	if ( orig_loc?$country_code )
		orig_geo$country_code = orig_loc$country_code;
	if ( orig_loc?$region )
		orig_geo$region = orig_loc$region;
	if ( orig_loc?$city )
		orig_geo$city = orig_loc$city;
#	if ( orig_loc?$latitude )
#		orig_geo$latitude = orig_loc$latitude;
#	if ( orig_loc?$longitude )
#		orig_geo$longitude = orig_loc$longitude;
    if ( orig_loc?$longitude && orig_loc?$latitude)
        orig_geo$point = [orig_loc$latitude, orig_loc$longitude];

	local resp_geo: GeoInfo;
	local resp_loc = lookup_location(c$id$resp_h);
	if ( resp_loc?$country_code )
		resp_geo$country_code = resp_loc$country_code;
	if ( resp_loc?$region )
		resp_geo$region = resp_loc$region;
	if ( resp_loc?$city )
		resp_geo$city = resp_loc$city;
#	if ( resp_loc?$latitude )
#		resp_geo$latitude = resp_loc$latitude;
#	if ( resp_loc?$longitude )
#		resp_geo$longitude = resp_loc$longitude;
    if ( orig_loc?$longitude && orig_loc?$latitude)
        orig_geo$point = [orig_loc$latitude, orig_loc$longitude];

	local geo_pair: GeoPair;
	geo_pair$orig = orig_geo;
	geo_pair$resp = resp_geo;

	c$conn$geo = geo_pair;

	}


event zeek_init() &priority=5
    {
    print("Starting Analisys");
    Log::create_stream(Scan::LOG, [$columns=Info]);
    }

event zeek_done()
    {
    print("Analisys Complete");
    }
