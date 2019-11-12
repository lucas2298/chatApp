const sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('./Server/database/chatbot.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err.message)
    }
    console.log("ahihi")
});
db.serialize(()=>{
    let sql = `select * from alltag
                where tag = ? and lock= ?`
    db.each(sql, ['advice', 'tuyendung'], (err, row) => {
        if (err) {
            throw err;
        }
        console.log(row)
    });
});
lock = {}
lock['ahihi'] = 1;
lock['ahuhu'] = 2;
if (!('ahuhi' in lock)) console.log("not in")
console.log(lock)