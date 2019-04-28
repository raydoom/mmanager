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
    $.get("/docker/container_option?server_ip=" + server_ip + "&server_port=" + server_port + "&container_id=" + container_id + '&container_name=' +  container_name + "&container_opt=" + opt, 
        function (data, status) {
        parse_result(data)
                    }
    );
}

/*重启supervisor管理的进程按钮点击事件*/
function process_opt(server_ip, server_port, process_name, opt) {
    $.get("/supervisor/process_option?server_ip=" + server_ip + "&server_port=" + server_port + "&process_name=" + process_name + "&process_opt=" + opt, 
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
    $.get("/jenkins/job_option?server_ip=" + server_ip + "&server_port=" + server_port + "&job_name=" + job_name + "&jenkins_opt=" + opt, 
        function (data,status) {
        parse_result(data)
                    }
    );
}


/*控制左侧sidebar展开和标签选中状态*/
window.onload = function() { 
var url = document.location.toString();
var pathname = window.location.pathname;
var showItem =pathname.split('/')[2];
var checkItem = "#nav-"+showItem;

  $(checkItem).parents("ul").collapse();
  $(checkItem).css('background','#428bca');
  $(checkItem).css('color','#FFF8F1');
 
}
