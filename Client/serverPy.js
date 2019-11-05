let express = require('express');
let socket = require('socket.io');
let bodyParser = require('body-parser');
let request = require('request-promise');
let spawn = require('child_process').spawn;

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

function decodeBase64(mess) {
    let buff = new Buffer(mess, 'base64');
    let messDecode = buff.toString('utf8');
    return messDecode;
}

io.on('connection', function(socket) {
    socket.on('chat', function(data){
        io.to(socket.id).emit('chat', data);
        // Xoa dau
        let mess = xoa_dau(data.message).toLowerCase();
        // Get answer from python
        getResponse(mess, socket.id)
        .then (function (messRes) {            
            let messDecode = decodeBase64(messRes);
            let messAnsw = "";
            let user = false;
            let selectID = 0;
            for (let i = 1; i < messDecode.length; i++) {
                if (messDecode[i] != "\n" && messDecode[i] != "+") messAnsw += messDecode[i];
                else 
                if (messDecode[i] == "+") {
                    io.to(socket.id).emit('chat', {
                        message: messAnsw,
                        isUser: false,
                        isSelectList: false,
                        id: 0
                    });
                    break;
                }
                else {
                    if (!user) {
                        user = true;
                        io.to(socket.id).emit('chat', {
                            message: messAnsw,
                            isUser: false,
                            isSelectList: false,
                            id: 0
                        });
                    }
                    else {
                        selectID++;
                        io.to(socket.id).emit('chat', {
                            message: messAnsw,
                            isUser: true,
                            isSelectList: true,
                            id: selectID
                        });
                    }
                    messAnsw = ""
                }
            }

        });

    });
});
