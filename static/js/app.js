/*
 * appjs.
 */

function parse_result(data) {
    if (data) {
        toastr.success('Action Success');
    } else {
        toastr.error('Action Failed');
    }
}

function container_opt(server_ip, server_port, container_id, container_name, opt) {
    $.get("/container_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id + '&container_name=' +  container_name + "&container_opt=" + opt, 
        function (data, status) {
        parse_result(data)
                    }
    );
}

function supervisor_app_opt(server_ip, server_port, supervisor_app, opt) {
    $.get("/supervisor_app_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&supervisor_app=" + supervisor_app + "&supervisor_opt=" + opt, 
        function (data,status) {
        parse_result(data)
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
        function (data,status) {
        parse_result(data)
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

/*window.onload = function() { 
  $("#collapse-ops-manage").addClass("show");
}

$(document).ready(function() {
    if(location.hash) {
        $('a[href=' + location.hash + ']').collapse('show');
    }
    $(document.body).on("click", "a[data-toggle]", function(event) {
        location.hash = this.getAttribute("href");
    });
});
$(window).on('popstate', function() {
    var anchor = location.hash || $("a[data-toggle=tab]").first().attr("href");
    $('a[href=' + anchor + ']').collapse('show');
});
*/


window.onload = function() { 
var url = document.location.toString();

if (url.search("dockerserver")>0)  {
  $("#collapse-server-action").collapse();
  $("#nav-dockerserver").css('background','#428bca');
  $("#nav-dockerserver").css('color','#FFF8F1');
}


if (url.search("supervisorserver")>0)  {
  $("#collapse-server-action").collapse();
  $("#nav-supervisorserver").css('background','#428bca');
  $("#nav-supervisorserver").css('color','#FFF8F1');
}

if (url.search("jenkinsserver")>0)  {
  $("#collapse-ops-manage").collapse();
  $("#nav-jenkinsserver").css('background','#428bca');
  $("#nav-jenkinsserver").css('color','#FFF8F1');
}

if (url.search("dirviewer")>0)  {
  $("#collapse-ops-manage").collapse();
  $("#nav-dirviewer").css('background','#428bca');
  $("#nav-dirviewer").css('color','#FFF8F1');
}

if (url.search("actionlog")>0)  {
  $("#collapse-ops-manage").collapse();
  $("#nav-actionlog").css('background','#428bca');
  $("#nav-actionlog").css('color','#FFF8F1');
}

if (url.search("account")>0)  {
  $("#collapse-setting").collapse();
  $("#nav-account").css('background','#428bca');
  $("#nav-account").css('color','#FFF8F1');
}

if (url.search("system")>0)  {
  $("#collapse-setting").collapse();
  $("#nav-dirviewer").css('background','#428bca');
  $("#nav-dirviewer").css('color','#FFF8F1');
}

}


　　