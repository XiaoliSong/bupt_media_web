const API_PREFIX = "/";

function upload_file(){
    let file = document.getElementById("input_file").files[0];
    let form = new FormData(); 
    if (file) {
        form.append("file", file);
    }
    else{
        alert("没有选择文件！");
        return;
    }
    axios.post(API_PREFIX+'file/upload', form, {
        method: 'post',
        headers: {'Content-Type': 'multipart/form-data'}
    }).then((res) => {
        if (res.data.code === 0) {
            alert("上传成功");
            window.location.reload();
        } 
        else {
            alert("code="+res.data.code+"，msg="+res.data.msg)
        }
    }).catch((error) => {
        alert(error);
    });
}

function delete_file(file_name){
    let form = new FormData(); 
    form.append('file_name', file_name)
    axios.post(API_PREFIX+'file/delete', form)
    .then(function (res) {
        if (res.data.code === 0) {
            alert("删除成功");
            window.location.reload();
        } 
        else {
            alert("code="+res.data.code+"，msg="+res.data.msg)
        }
    })
    .catch(function (error) {
        alert(error);
    });
}

function display_file_list(file_arr){
    let obj =document.getElementById("file_list_body")
    file_arr.forEach(function(file) {
        let new_child = document.createElement("tr")
        new_child.innerHTML = "";
        new_child.innerHTML += "<td>" + file['time'] +"</td>";
        new_child.innerHTML += "<td>" + file['name'] +"</td>";
        new_child.innerHTML += "<td>" + file['size'] +"</td>";
        new_child.innerHTML += "<td>" + "<a href='"+API_PREFIX+"file/download?file_name="+file['name'] + "'>下载</a>" +"</td>";
        new_child.innerHTML += "<td>" + "<button class='delete_btn' onclick='delete_file(\""+file['name']+"\")'>删除</button>" +"</td>";
        obj.appendChild(new_child);
    });
}

(function(){
    axios.get(API_PREFIX+"file/list")
    .then((res) => {
        if (res.data.code === 0) {
            data = res.data.data;
            if (data.files.length > 0){
                display_file_list(data.files);
            }
        } 
        else {
            alert("code="+res.data.code+"，msg="+res.data.msg)
        }
    }).catch((error) => {
        alert(error);
    });
})()