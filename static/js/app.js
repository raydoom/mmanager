/**
 * appjs.
 */
function reload_window() {
    window.location.reload()

}

function container_opt(server_ip, server_port, container_id, container_name, opt) {
    $.get("/container_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id + '&container_name=' +  container_name + "&container_opt=" + opt, 
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

/*function tail_container_log(server_ip, server_port, container_id) {
    window.open("/tail_container_log/?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id)
}
*/
/*
function tail_supervisor_app_log(server_ip, server_port, supervisor_app) {
    window.open("/tail_supervisor_app_log/?server_ip=" + server_ip + "&server_port=" + server_port + "&supervisor_app=" + supervisor_app)
}*/

function jenkins_job_opt(server_ip, server_port, job_name, opt) {
    $.get("/jenkins_job_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&job_name=" + job_name + "&jenkins_opt=" + opt, 
        function () {
        reload_window()
                    }
    );
}

/*function text_viewer(file_name, current_dir){
    window.open("/textviewer/?dist=" + current_dir + file_name)   
}

function dir_viewer(to_dir_name, current_dir){
    this.location.href = ("/dirviewer/?dist=" + current_dir + to_dir_name)

}

function file_download(file_name, current_dir){
    window.open("/filedownload/?filepath="+ current_dir + file_name)

}
*/