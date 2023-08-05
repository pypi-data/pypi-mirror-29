function generateSpiderList(list) {
    var tableBody = $("#spiderListDataTableBody");
    tableBody.children().remove();
    for (var i = 0; i < list.length; i++) {
        var tr = $("<tr></tr>");
        tr.append($("<td>" + list[i].spider_name + "</td>"));
        tr.append($("<td>" + list[i].project_name + "</td>"));
        tr.append($("<td>" + list[i].latest_project_version + "</td>"));
        tr.append($("<td>" + list[i].pending_job_amount + "</td>"));
        tr.append($("<td>" + list[i].running_job_amount + "</td>"));
        tr.append($("<td>" + list[i].finished_job_amount + "</td>"));
        tr.append($("<td><button class='btn btn-primary btn-lg' data-toggle='modal' " +
            "onclick='bindInfoToLogModal(\"" + list[i].project_name + "\",\"" + list[i].spider_name + "\")' " +
            "data-target='#logModal'>" + "Log</button></td>"));
        tableBody.append(tr);
    }
}

function ajax_spider_list() {
    $.ajax({
        url: "/scrapyd/spider/list",
        type: "GET",
        success: function (data) {
            timeout_alert(data[polling_info.failure_message_key]);
            generateSpiderList(data);
        },
        error: function (xhr, message, throwable) {
            ajax_error_alert(xhr.status, message);
        }
    });
}

invoke_polling(ajax_spider_list);

$("#spiderListDataTable").DataTable();