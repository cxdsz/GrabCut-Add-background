var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var PythonShell = require('python-shell');

var multiparty = require('multiparty');


var multer = require('multer');
var upload = multer({ dest: 'uploads/' }) // 입력된 파일 저장 위치

app.locals.pretty = true;
app.set('view engine', 'ejs');
app.set('views', './views');

app.use(express.bodyParser());
app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended: false}));

app.get('/upload', function(req,res){
	res.render('upload');
});

app.post('/upload_image', (req, res) => {
    let form = new multiparty.Form({
        autoFiles: true,
        uploadDir: './uploadss',
        maxFilesSize: 1024 * 1024 * 5 // 허용 파일 사이즈 최대치
    });
		console.log(req.files);
		console.log(req.files.originalFilename);


    form.parse(req, (error, fields, files) => {
    	// 파일 전송이 요청되면 이곳으로 온다.
        // 에러와 필드 정보, 파일 객체가 넘어온다.


    	res.json('file uploaded'); // 파일과 예외 처리를 한 뒤 브라우저로 응답해준다.
    });
});


////////////////////////////////////////



app.get('/test', function(req,res){
		PythonShell.run('grabcut.py',
		    {
		      mode: 'text',
		      pythonPath: '',
		      pythonOptions: ['-u'],
		      scriptPath: '/Users/jaejin/dev/Opensoftware',
		      args: ['/Users/jaejin/dev/Opensoftware/test/cat.jpg']

		    }
		    , function (err, results){
		    if (err) throw err;

		    console.log('results: %j', results);
		    res.render('view',{
		      test: results
		    })

		  });
})


app.listen(3000, function(){
	console.log('Conneted 3000 port!! ');
});
