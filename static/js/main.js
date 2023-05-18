// # 역할 분담
// # 최신혜 : 페이지 이동
// # 박행복 : 방명록 조회
// # 이경원 : 방명록 작성
// # 조우진 : 방명록 수정/삭제
// # 박수빈 : 메인 페이지 프론트엔드
// # 공통 : 개인 프로필 프론트엔드
//----------------------------------------------------------------- 조우진
// 
function show_comment() {
    let name = $('#name').text();
    console.log(name);
    switch (name) {
        case '조우진':
            fetch('/guestbook?name=' + name).then((res) => res.json()).then((data) => {
                let rows = data['result']
                commentIdx = 1;
                $('#comment-list').empty()
                rows.forEach(a => {
                    let id = a['id'];
                    let comment = a['comment'];
                    let password = a['password'];
                    // let edittime = a['timestamp'];
                    let objectId = a['_id']
                    let temp_html = `
                    <ul class="list-group list-group-flush">
                        <div class="row">
                            <div class="col">
                                <label for="list-group-item" class="commentId" id="editid-${commentIdx}">${id}</label>
                            </div>
                            <div class="col">
                                 <input type="text" class="form-control" id="editpassword-${commentIdx}" value="" placeholder="PW">
                            </div>
                        </div>
                        <li class="list-group-item">
                            <div class="row">
                                <div class="col-10">
                                    <input type="text" class="form-control-plaintext" id="editcomment-${commentIdx}" disabled
                                        value="${comment}">
                                </div>
                                <div class="col-2">
                                    <!-- 내용변경 -->
                                    <div class="button-group">
                                        <button id="edit-button-${commentIdx}" class="edit-button-${commentIdx}" onclick="editbutton_clicked(this)" value="${commentIdx}" data-id="${objectId}">✏️</button>
                                        <button id="done-button-${commentIdx}" style="display: none;" class="done-button-${commentIdx}" onclick="donebutton_clicked(this)" value="${commentIdx}" data-id="${objectId}">완료</button>
                                        <button id="delete-button-${commentIdx}" class="delete-button-${commentIdx}" onclick="deletebutton_clicked(this)" value="${commentIdx}" data-id="${objectId}">❌</button>
                                    </div>
        
                                </div>
                            </div>
                        </li>
                    </ul>`
                    $('#comment-list').append(temp_html)
                    commentIdx++;
                });
            });
            break;

        case '박수빈':
            fetch('/guestbook?name=' + name).then((res) => res.json()).then((data) => {
                let rows = data['result']
                commentIdx = 1;
                $('#comment-list').empty()
                rows.forEach(a => {
                    let id = a['id'];
                    let comment = a['comment'];
                    let password = a['password'];
                    // let edittime = a['timestamp'];
                    let objectId = a['_id']

                    let temp_html = `<ul class="list-group list-group-flush">
                                        <div class="row">
                                            <div class="col">
                                                <label for="list-group-item" class="commentId" id="editid-${commentIdx}">${id}</label>
                                            </div>
                                            <div class="col">
                                                <input type="text" class="form-control" id="editpassword-${commentIdx}" value="" placeholder="PW">
                                            </div>
                                        </div>
                                        <li class="list-group-item">
                                            <div class="row">
                                                <div class="col-10">
                                                    <input type="text" class="form-control-plaintext" id="editcomment-${commentIdx}" disabled
                                                        value="${comment}">
                                                </div>
                                                <div class="col-2">
                                                    <!-- 내용변경 -->
                                                    <div class="button-group">
                                                        <button id="edit-button-${commentIdx}" class="edit-button-${commentIdx}" onclick="editbutton_clicked(this)" value="${commentIdx}" data-id="${objectId}">✏️</button>
                                                        <button id="done-button-${commentIdx}" style="display: none;" class="done-button-${commentIdx}" onclick="donebutton_clicked(this)" value="${commentIdx}" data-id="${objectId}">완료</button>
                                                        <button id="delete-button-${commentIdx}" class="delete-button-${commentIdx}" onclick="deletebutton_clicked(this)" value="${commentIdx}" data-id="${objectId}">❌</button>
                                                    </div>
                        
                                                </div>
                                            </div>
                                        </li>
                                    </ul>`
                    $('#comment-list').append(temp_html)

                })
            });
            break;

        case '박행복':
            fetch('/guestbook?name=' + name).then((res) => res.json()).then((data) => {
                let rows = data['result']
                $('#comment-list').empty()
                let commentIdx=1;
                rows.forEach(a => {

                    let name = a['name']
                    let id = a['id']
                    let pw = a['password']
                    let comment = a['comment']
                    let num = a['num']
                    let objectId = a['_id'];
                    console.log(id, pw, comment, num)
                    if ($('#name').text() == a['name']) {
                        let temp_html = `<div class="card">
                                            <div class="card-body">
                                                <blockquote class="blockquote mb-0">
                                                <p>${comment}</p>
                                                <footer class="blockquote-footer">${id}</footer>
                                                </blockquote>
                                                <div class="d-flex justify-content-end">
                                                <button onclick="editbutton_clicked(this)" type="button" class="btn btn-outline-secondary" value="${commentIdx}" data-id="${objectId}"   >수정</button>
                                                <button onclick="editbutton_clicked(this)" type="button" class="btn btn-outline-secondary" style="display:none;"value="${commentIdx}" data-id="${objectId}"  >완료</button>
                                                <button onclick="deletebutton_clicked(this))" type="button" class="btn btn-outline-secondary"value="${commentIdx}" data-id="${objectId}" >삭제</button>
                                                </div>
                                                <div class="input-group flex-nowrap">
                                                <span class="input-group-text" id="addon-wrapping">PW</span>
                                                <input type="text" class="form-control" placeholder="Password" aria-label="Username" aria-describedby="addon-wrapping">
                                                </div>
                                            </div>
                                        </div>`
                        $('#comment-list').append(temp_html)
                    }

                })
            });
            break;


    }

}

function savebutton_clicked() {
    let name = $('#name').text(); //페이지 주인 이름
    let comment = $('#comment').val();//댓글내용
    let id = $('#id').val(); // 아이디 입력란의 값을 가져옴
    let password = $('#password').val(); // 비밀번호 입력란의 값을 가져옴
    console.log(name, comment, id, password)
    let formData = new FormData();
    formData.append("name_give", name);
    formData.append("comment_give", comment);
    formData.append("id_give", id);
    formData.append("password_give", password);
    formData.append()

    fetch('/guestbook', { method: "POST", body: formData, }).then((response) => response.json()).then((data) => {
        console.log(data)
        alert(data["msg"]); // app.py(서버)로부터 댓글정보를 반환(return)받아 돌아오는 데이터
        window.location.reload();
        // 방명록 작성되었을 때 새로고침 하지 않고 방명록 값만 가져올 방법이 있는지 찾아보기

    });
}

function editbutton_clicked(button) {
    // 클릭한 버튼의 id 가져오기위해 button을 인자값으로 받음
    //button.value : <button>태그의 value($commentIdx) ex)방명록의 번호(1, 2, 3,...)
    let objectId = button.getAttribute('data-id')
    let targetpassword = $('#editpassword-' + button.value).val();                   //입력한 pw
    console.log(objectId)

    let formData = new FormData();
    formData.append("objectId_give", objectId);
    formData.append("targetpassword_give", targetpassword);
    fetch('/guestbook/3', { method: "POST", body: formData, }).then((response) => response.json()).then((data) => {
        // 해당 버튼에 대한 처리
        if (data["result"] == "success") {
            var buttonId = $(this).attr('id');
            $('#edit-button-' + button.value).hide();
            $('#done-button-' + button.value).show();

            $('#editcomment-' + button.value).addClass('form-control');
            $('#editcomment-' + button.value).removeClass('form-control-plaintext');
            $('#editcomment-' + button.value).prop('disabled', false);

        }
        else if (data["result"] == "fail") {
            alert(data["msg"]);
        }
    });
}

function donebutton_clicked(button) {
    let objectId = button.getAttribute('data-id')
    let updatecomment = $('#editcomment-' + button.value).val()
    let targetpassword = $('#editpassword-' + button.value).val();

    let formData = new FormData();
    formData.append("objectId_give", objectId);
    formData.append("updatecomment_give", updatecomment)
    formData.append("targetpassword_give", targetpassword);
    fetch('/guestbook/3', { method: "PUT", body: formData, }).then((response) => response.json()).then((data) => {
        // 해당 버튼에 대한 처리
        if (data["result"] == "success") {
            alert(data["msg"]);
            window.location.reload();
        }
        else if (data["result"] == "fail") {
            alert(data["msg"]);
        }
    });
}

function deletebutton_clicked(button) {
    // 클릭한 버튼의 id 가져오기위해 button을 인자값으로 받음
    //button.value : <button>태그의 value($commentIdx) ex)방명록의 번호(1, 2, 3,...)
    let objectId = button.getAttribute('data-id')
    let targetpassword = $('#editpassword-' + button.value).val();                   //입력한 pw
    console.log(objectId)

    let formData = new FormData();
    formData.append("objectId_give", objectId);
    formData.append("targetpassword_give", targetpassword);

    fetch('/guestbook/2', { method: "DELETE", body: formData, }).then((response) => response.json()).then((data) => {
        console.log(data)
        // 해당 버튼에 대한 처리
        if (data["result"] == "success") {
            alert(data["msg"]);
            window.location.reload();
        }
        else if (data["result"] == "fail") {
            alert(data["msg"]);
        }
    });
}
//----------------------------------------------------------------- 조우진

//----------------------------------------------------------------- 박수빈
function save_comment() {

    let name = $('#name').text()
    let id = $('#id').val()
    let password = $('#password').val()
    let comment = $('#comment').val()

    let formData = new FormData();
    formData.append("name_give", name);
    formData.append("id_give", id);
    formData.append("password_give", password);
    formData.append("comment_give", comment);

    fetch('/guestbook', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        alert(data["msg"]);
        window.location.reload()
    });
}
// function show_comment() {
//     let name = $('#name').text();
//     fetch('/guestbook?name=' + name).then((res) => res.json()).then((data) => {

//         let rows = data['result']
//         $('#comment-list').empty()
//         rows.forEach((a) => {
//             // let name = a['name']
//             let id = a['id']
//             // let password = a['password']
//             let comment = a['comment']

//             let temp_html = `<div class="card" style="margin-top: 0;">
//                                 <div class="card-body" style="height: 100%;">
//                                     <blockquote class="blockquote mb-0">
//                                         <p>${comment}</p>
//                                         <footer class="blockquote-footer">${id}</footer>
//                                     </blockquote>
//                                 </div>
//                             </div>`
//             $('#comment-list').append(temp_html)

//         })
//     });
// }
//--------------------------------------------------------------- 박수빈
