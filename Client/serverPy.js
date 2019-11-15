let express = require('express');
let socket = require('socket.io');
let bodyParser = require('body-parser');
let request = require('request-promise');

// App setup
let app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
let server = app.listen(process.env.PORT || 4000, function() {
});

// Static files
app.use(express.static('public'));

// async function
// Get answer from server
async function getResponse(req, id) {
    let options = {
        method: 'POST',
        // local
        uri: 'http://localhost:4001/postdata',
        // live
        // uri: 
        body: req+'+'+id,
        json: true
    };
    let returndata = await request(options)
    return returndata;
}

// Socket setup
let io = socket(server);

// Xoa dau tieng viet
function xoa_dau(str) {
    str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a");
    str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e");
    str = str.replace(/ì|í|ị|ỉ|ĩ/g, "i");
    str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o");
    str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u");
    str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y");
    str = str.replace(/đ/g, "d");
    str = str.replace(/À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ/g, "A");
    str = str.replace(/È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ/g, "E");
    str = str.replace(/Ì|Í|Ị|Ỉ|Ĩ/g, "I");
    str = str.replace(/Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ/g, "O");
    str = str.replace(/Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ/g, "U");
    str = str.replace(/Ỳ|Ý|Ỵ|Ỷ|Ỹ/g, "Y");
    str = str.replace(/Đ/g, "D");
    return str;
}

function stringToTags(mess) {
    tags = [];
    s = ""
    for (i = 1; i < mess.length; i++) 
    if (mess[i] != '+') {
        s += mess[i]
    }
    else {
        tags.push(s);
        s = ''
    }
    tags.push(s)
    return tags;
}

// Connect to database
let mysql = require('mysql');
let connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "chatbot"
});

lock = {}

io.on('connection', function(socket) {
    let userID = socket.id;
    socket.on('chat', function(data){
        if (!(userID in lock)) {
            lock[userID] = ''
        }
        io.to(socket.id).emit('chat', data);
        // Xoa dau
        let mess = xoa_dau(data.message).toLowerCase();        
        // Get tags from python
        getResponse(mess, socket.id)
        .then (function (messRes) {
            // Python return a string has type +tag1+tag2+tagn
            // We have to change it to an array [tag1, tag2, tagn]
            let tags = stringToTags(messRes);
            // If this user is new
            if (lock[userID] == '') {
                // Get all tag from database
                let sql = 'select * from alltag';
                connection.query(sql, function(err, rows){
                    if (err) {
                        console.log(err)
                        return;
                    }
                    // With each tag, if tag we recived from python has private = no
                    // send response to client
                    rows.forEach(function(row){
                        for (i = 0; i < tags.length; i++) {
                            if (tags[i] == row.tag) {
                                if (row.private == 'no') {
                                    lock[userID] = row.locks;
                                    question = row.question;
                                    io.to(userID).emit('chat', {
                                        message: row.response,
                                        isUser: false,
                                        isSelectList: false,
                                        id: 0
                                    });                                    
                                    if (question != '') {
                                        io.to(userID).emit('chat', {
                                            message: question,
                                            isUser: false,
                                            isSelectList: false,
                                            id: 0
                                        });
                                    }
                                    sql = "select selects from selectlist where tag = ?"
                                    arg = [tags[i]]
                                    connection.query(sql, arg, function(err, rowSelects){
                                        if (err) {
                                            console.log(err)
                                            return;
                                        }
                                        rowSelects.forEach(function(rowSelect){
                                            io.to(userID).emit('chat', {
                                                message: rowSelect.selects,
                                                isUser: false,
                                                isSelectList: true,
                                                id: 0
                                            });
                                        });
                                    });
                                }
                                return;
                            }
                        }                        
                    });
                });
            }
            else {
                let sql = 'select * from keyunlock';
                connection.query(sql, function(err, rows){
                    if (err) {
                        console.log(err)
                        return;
                    }
                    // With each tag, if tag we recived from python has lock = key
                    // send response to client
                    rows.forEach(function(row) {
                        for (i = 0; i < tags.length; i++) 
                            if (tags[i] == row.tag && lock[userID] == row.keyUnlock) {
                                let messRes = '';                                
                                sql = 'select * from alltag where tag = ?'
                                arg = [tags[i]]
                                connection.query(sql, arg, function(err, rowtags){
                                    rowtags.forEach(function(rowtag){
                                        lock[userID] = rowtag.locks;
                                        messRes = rowtag.response;
                                        question = rowtag.question;
                                    });
                                });
                                io.to(userID).emit('chat', {
                                    message: messRes,
                                    isUser: false,
                                    isSelectList: false,
                                    id: 0
                                });
                                console.log(tags[i])
                                console.log(lock[userID])
                                console.log(question)
                                console.log(messRes)
                                console.log("ahihi\n")
                                if (question != '') {
                                    io.to(userID).emit('chat', {
                                        message: question,
                                        isUser: false,
                                        isSelectList: false,
                                        id: 0
                                    });
                                }
                                // sql = "select selects from selectlist where tag = ?"
                                // arg = [tags[i]]
                                // connection.query(sql, arg, function(err, rowSelects){
                                //     if (err) {
                                //         console.log(err)
                                //         return;
                                //     }
                                //     rowSelects.forEach(function(rowSelect){
                                //         io.to(userID).emit('chat', {
                                //             message: rowSelect.selects,
                                //             isUser: false,
                                //             isSelectList: true,
                                //             id: 0
                                //         });
                                //     });
                                // });
                                // return;
                            }
                    });
                });
            }
        });
    });
});
