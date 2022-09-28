import DAST

Jenkinsfile_path = "/home/bibim/bibim/Jenkins-files/"
library_path = "/home/bibim/bibim/components/"

def call_generator(tool_list, jenkinsfile_name):
    jenkinsfile = open(Jenkinsfile_path + jenkinsfile_name, 'w')
    """
    for tool in tool_list:
        print(globals())
        list_buffer = globals()[tool+'_generator']()
        for component in list_buffer:
            component_file = open(library_path+component[0]+'/'+component[1], 'r')
            jenkinsfile.write(component_file.read())
    """
    list_buffer = DAST.ZAP_generator()
    for component in list_buffer:
            component_file = open(library_path+component[0]+'/'+str(component[1]), 'r')
            jenkinsfile.write(component_file.read())

def get_input(input_json):
    tool_list = []

    for stage in input_json:
        for tool in stage:
            if input_json[stage][tool]:
                tool_list.append(stage+'.'+tool)
    
    call_generator(tool_list)


if __name__ == "__main__":
    call_generator(['ZAP'], 'test')
    