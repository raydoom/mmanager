/**
 * appjs.
 */
function reload_window() {
    window.location.reload()

}

function container_opt(server_ip, server_port, container_id, opt) {
    $.get("/container_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id + "&container_opt=" + opt, 
        function () {
        reload_window()
                    }
    );
}

function supervisor_app_opt(server_ip, server_port, supervisor_app, opt) {
    $.get("/supervisor_app_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&supervisor_app=" + supervisor_app + "&supervisor_opt=" + opt, 
        function (data,status) {
        reload_window()
                    }
    );
}

function tail_container_log(server_ip, server_port, container_id) {
    window.open("/tail_container_log/?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id)
}

function tail_supervisor_app_log(server_ip, server_port, supervisor_app) {
    window.open("/tail_supervisor_app_log/?server_ip=" + server_ip + "&server_port=" + server_port + "&supervisor_app=" + supervisor_app)
}

function text_viewer(file_name, current_dir){
    window.open("/text_viewer/?file_name="+file_name + "&current_dir=" + current_dir)   
}

function dir_viewer(to_dir_name, current_dir){
    window.open("/dir_viewer/?to_dir_name="+ to_dir_name + "&current_dir=" + current_dir)

}