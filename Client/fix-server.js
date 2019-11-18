let express = require('express');
let socket = require('socket.io');
let bodyParser = require('body-parser');
let request = require('request-promise');
let func = require('./function');

// App setup
let app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
let server = app.listen(process.env.PORT || 4000, function() {
});

// Static files
app.use(express.static('./Client/public'));

// Socket setup
let io = socket(server);

// Connect to database
const pool = require('./test');

lock = {}

// Get response with lock = ''
async function getResponseHasNoLock (tags, userID) {
    sql = 'select * from alltag';
    arg = [];
    rows = await pool.query(sql, arg);
    for (i in rows) {
        row = rows[i];
        for (j in tags) {
            tag = tags[j];
            if (tag == row['tag']) {
                lock[userID] = row['locks'];
                io.to(userID).emit('chat', {
                    message: row['response'],
                    isUser: false,
                    isSelectList: false,
                    id: 0
                });
                getSelectList(tag, userID);
                return;
            }
        }
    }
}
// Get response with lock != ''
async function getResponseHasLock(tags, userID, LOCK) {
    sql = 'select * from keyunlock where keyunlock = ?';
    arg = [LOCK];
    rows = await pool.query(sql, arg);
    for (i in rows) {
        row = rows[i];
        for (j in tags) {
            tag = tags[j];
            if (row['tag'] == tag && row['keyUnlock'] == LOCK)  {
                sql = 'select * from alltag where tag = ?';
                arg = [tag];
                rowTag = await pool.query(sql, arg);
            }
        }
    }
}
// Get select list
async function getSelectList(tag, userID) {
    sql = 'select * from selectlist where tag = ?';
    arg = [tag];
    rows = await pool.query(sql, arg);
    for (i in rows) {
        row = rows[i];
        if (row['tag'] == tag) {
            io.to(userID).emit('chat', {
                message: row['selects'],
                isUser: false,
                isSelectList: true,
                id: 0
            });
        }
    }
}

io.on('connection', function(socket) {
    let userID = socket.id;
    socket.on('chat', function(data){
        if (!(userID in lock)) {
            lock[userID] = ''
        }
        io.to(socket.id).emit('chat', data);
        // Xoa dau
        let mess = func.xoa_dau(data.message).toLowerCase();        
        // Get tags from python
        func.getAllTag(mess, socket.id)
        .then (function (messRes) {
            let tags = func.stringToTags(messRes);
            // If this user is new
            if (lock[userID] == '') {
                // Get response
                getResponseHasNoLock(tags, userID);
            }
            else {
                // Get response
                getResponseHasLock(tags, userID, lock[userID]);
            }
        });
    });
});
