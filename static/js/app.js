/*
 * appjs.
 */
 
/*操作返回状态接收和操作结果提示*/
function parse_result(data) {
    if (data) {
        toastr.success('Action Success');
        console.log(data)
    } else {
        toastr.error('Action Failed');
    }
}

/*重启容器按钮点击事件*/
function container_opt(server_ip, server_port, container_id, container_name, opt) {
    $.get("/container_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id + '&container_name=' +  container_name + "&container_opt=" + opt, 
        function (data, status) {
        parse_result(data)
                    }
    );
}

/*重启supervisor管理的进程按钮点击事件*/
function process_opt(server_ip, server_port, process_name, opt) {
    $.get("/process_opt/?server_ip=" + server_ip + "&server_port=" + server_port + "&process_name=" + process_name + "&process_opt=" + opt, 
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
function tail_process_name_log(server_ip, server_port, process_name) {
    window.open("/tail_process_name_log/?server_ip=" + server_ip + "&server_port=" + server_port + "&process_name=" + process_name)
}*/

/*触发henkins任务构建按钮点击事件*/
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



/*控制左侧sidebar展开和标签选中状态*/
window.onload = function() { 
var url = document.location.toString();
var pathname = window.location.pathname;
var showItem =pathname.substring(1,pathname.length-1);
var checkItem = "#nav-"+showItem;

  $(checkItem).parents("ul").collapse();
  $(checkItem).css('background','#428bca');
  $(checkItem).css('color','#FFF8F1');
 
}


　　