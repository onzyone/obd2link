import os
import file_io as file_io

def get_globals():
    ph = file_io.PropertiesHelper()

    obd2_config_home = '/mnt/application/obd2link/obd2link/config'

    application_properties_file = os.path.join(obd2_config_home, 'application.properties')
    application_properties = ph.get_yaml_config(filename=application_properties_file, use_full_path=True)

    sensors_file = os.path.join(obd2_config_home, 'codes.properties')
    sensors = ph.get_yaml_config(filename=sensors_file, use_full_path=True)

    logger_file = os.path.join(obd2_config_home, 'logger.properties')
    logger_config = ph.get_yaml_config(filename=logger_file, use_full_path=True)
#    log_file = logger_config.get('handlers').get('logfile')
#    dh.update_dict(log_file, 'filename', (rv.get('loggerFolder') + '/your_log_file_name.log'))


    #print application_properties
    #print sensors
    #print logger_config

    return application_properties, sensors, logger_config
