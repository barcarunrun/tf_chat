var now = new Date();
var NextAnswerId = 0;



//フェードの処理
function fadeIn() {
    $('#chat').fadeIn();
}

function fadeOut() {
    $('#buttom').fadeOut();
}

function fadeOutChat() {
    $('.chat').fadeOut();
}

function fadeIn(node, duration) {
    // display: noneでないときは何もしない
    if (getComputedStyle(node).display !== 'none') return console.log(5);

    // style属性にdisplay: noneが設定されていたとき
    if (node.style.display === 'none') {
        node.style.display = 'block';

    } else {
        node.style.display = 'block';

    }
    node.style.opacity = 0;

    var start = performance.now();


    requestAnimationFrame(function tick(timestamp) {
        // イージング計算式（linear）
        var easing = (timestamp - start) / duration;

        // opacityが1を超えないように
        node.style.opacity = Math.min(easing, 1);

        // opacityが1より小さいとき
        if (easing < 1) {
            requestAnimationFrame(tick);

        } else {
            node.style.opacity = '';

        }
    });
}


//スクロールのための処理
function scroll() {
    scrollingElement = document.querySelector('#bms_messages');
    scrollingElement.scrollTop = scrollingElement.scrollHeight;

}


//postするLogデータの編集
function postForm(userId, Withdrawal) {
    var Para = document.getElementById("message").value;
    var flag=false;
    for (var i in jsonGet) {
        if (jsonGet[i]['Keyword'] != '') {
            if (Para.match(jsonGet[i]['Keyword'])) {
                document.getElementById("AnswerNo").value = jsonGet[i]['id'];
                document.getElementById("Answer").value = jsonGet[i]['answer'];
                var flag=true;
            }
        }
    }

    if(flag==false)
    {   var superHeroes = request.response;
    var str = JSON.stringify(superHeroes);

         var  jsonGet=str
        console.log('80jsonGet:'+jsonGet)
        document.getElementById("AnswerNo").value = jsonGet[0]['id'];
        document.getElementById("Answer").value = jsonGet[0]['answer'];
    }
    document.getElementById("userId").value = userId;
    document.getElementById("Question").value = document.getElementById("message").value;
    document.getElementById("Withdrawal").value = Withdrawal;
}

//Qを表示
function insertDataRight(Para) {

    var div = document.querySelector('#bms_messages');

    var bms_message_text = document.createElement('div');
    bms_message_text.className = 'bms_message_text';
    bms_message_text.innerText = Para;


    var bms_message_content = document.createElement('div');
    bms_message_content.className = 'bms_message_content';
    bms_message_content.appendChild(bms_message_text);

    var bms_message_box = document.createElement('div');
    bms_message_box.className = 'bms_message_box';
    bms_message_box.appendChild(bms_message_content);

    var bms_message_bms_right = document.createElement('div');
    bms_message_bms_right.className = 'bms_message bms_right';
    bms_message_bms_right.appendChild(bms_message_box);

    div.appendChild(bms_message_bms_right);

}

//Aを表示
function insertDataLeft(Response, URL, Para) {

    var div = document.querySelector('#bms_messages');
    var hotText = Response;
    var URL = URL;

    var bms_message_text = document.createElement('div');
    bms_message_text.className = 'bms_message_text';
    if (URL == undefined) {

        bms_message_text.innerHTML = hotText;
    }
    else if(URL ==''){
        bms_message_text.innerHTML = hotText;
    }
    else {
        bms_message_text.innerHTML = hotText.link(URL);
    }

    var bms_message_content = document.createElement('div');
    bms_message_content.className = 'bms_message_content';
    bms_message_content.appendChild(bms_message_text);

    var bms_message_box = document.createElement('div');
    bms_message_box.className = 'bms_message_box';
    bms_message_box.appendChild(bms_message_content);

    var bms_message_bms_left = document.createElement('div');
    bms_message_bms_left.className = 'bms_message bms_left';
    bms_message_bms_left.appendChild(bms_message_box);

    div.appendChild(bms_message_bms_left);
    scroll();

}

//入力されたメッセージを表示
function addReturnMessage() {
    var messeagePara = document.getElementById("message").value;
    insertDataRight(messeagePara);
    return messeagePara;
}

//ロジックを用いて表示
function addMessage() {
    var idPara = 0;
    var ReturnNum = 0;
     //console.log('jsonGet123:'+jsonGet[0]);
    for (var i in jsonGet) {
        if(idPara!=0){
            console.log('kokoidPara:'+idPara)
            break;
        }
        idPara = MakeReturn(i)
        if(idPara!=0){
             console.log('ReturnNum:'+ReturnNum)
             ReturnNum=idPara
        }
    }
    console.log('5678ReturnNum'+ReturnNum)
    console.log('jsonGet[ReturnNum][question][Q1]'+jsonGet[ReturnNum]['question']['Q1'])

    if (ReturnNum == 0) {
        insertDataLeft(jsonGet[0]['answer'], jsonGet[0]['url'])
    }
    console.log('ReturnNum下:'+ReturnNum)
    return ReturnNum
}

var jsonGet="";
//var jsonGet=document.getElementById('request').innerHTML;
//ボタンを押下時に実行
function Execute() {
    var huga = 0;
    parapara=document.getElementById('request').innerHTML;

    var para = addReturnMessage()

    var hoge = setInterval(
        function () {

            NextAnswerId = addMessage();
              if(jsonGet[NextAnswerId]['question']['Q1']==' ')
              {
                //ReturnがなにもなければNextAnswerIdを0にする（ストーリーの処理ではない）
                NextAnswerId=0;
                console.log('yesuuuuuuuuuu')
                console.log('NextAnswerId:'+NextAnswerId)
              }

            console.log('123456789NextAnswerId:'+NextAnswerId)
            scroll()
            huga++;
            //終了条件
            if (huga == 1) {
                clearInterval(hoge);
                document.getElementById("message").value = "";
            }
        }
        , 1000);
    scroll();
    console.log('End')


}

//×ボタン押下時の処理
function Delete() {
    var element = document.getElementById("bms_messages");

    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
    insertDataLeft('何かお手伝い致しましょうか?');
}


function MakeReturn(id) {
    var Para = document.getElementById("message").value;
    var Returnid = 0;
    console.log('NextAnswerId:' + NextAnswerId+'Para:'+Para)

    if (NextAnswerId != 0) {
        console.log('対話')
      //  console.log('jsonGet[NextAnswerId][\'question\']:' + jsonGet[NextAnswerId]['question']['Q1'])
        if (jsonGet[NextAnswerId]['question']['Q1'] != ' ') {
            if (Para.match(jsonGet[NextAnswerId]['question']['Q1'])) {
                console.log('A1')
                insertDataLeft('こちらでいかがでしょうか',);
                //console.log('jsonGet[NextAnswerId][question][A1]:'+jsonGet[NextAnswerId]['NextAnswerNo']['A1'])
                var NextNo=jsonGet[NextAnswerId]['NextAnswerNo']['A1'];
                response = jsonGet[NextNo]['answer'];
                URL = jsonGet[NextNo]['url'];
                insertDataLeft(response, URL);
                Returnid = jsonGet[NextNo]['id'];
            }
        }
        if (jsonGet[NextAnswerId]['question']['Q2'] != ' ') {
            if (Para.match(jsonGet[NextAnswerId]['question']['Q2'])) {
                console.log('A2')
                insertDataLeft('こちらでいかがでしょうか',);
                var NextNo=jsonGet[NextAnswerId]['NextAnswerNo']['A2'];
                response = jsonGet[NextNo]['answer'];
                URL = jsonGet[NextNo]['url'];
                insertDataLeft(response, URL);
                Returnid = jsonGet[NextNo]['id'];
            }
        }
         if (jsonGet[NextAnswerId]['question']['Q3'] != ' ') {
            if (Para.match(jsonGet[NextAnswerId]['question']['Q3'])) {
                console.log('A3')
                insertDataLeft('こちらでいかがでしょうか',);
                var NextNo=jsonGet[NextAnswerId]['NextAnswerNo']['A3'];
                response = jsonGet[NextNo]['answer'];
                URL = jsonGet[NextNo]['url'];
                insertDataLeft(response, URL);
                Returnid = jsonGet[NextNo]['id'];
            }
        }
         if (jsonGet[NextAnswerId]['question']['Q4'] != ' ') {
            if (Para.match(jsonGet[NextAnswerId]['question']['Q4'])) {
                console.log('A4')
                insertDataLeft('こちらでいかがでしょうか',);
                console.log('NextAnswerId:'+NextAnswerId)


                var NextNo=jsonGet[NextAnswerId]['NextAnswerNo']['A4'];
                console.log('NextNo:'+NextNo)

                response = jsonGet[NextNo]['answer'];
                URL = jsonGet[NextNo]['url'];
                insertDataLeft(response, URL);
                Returnid = jsonGet[NextNo]['id'];
            }
        }
         if (jsonGet[NextAnswerId]['question']['Q5'] != ' ') {
            if (Para.match(jsonGet[NextAnswerId]['question']['Q5'])) {
                console.log('A5')
                insertDataLeft('こちらでいかがでしょうか',);
               var NextNo=jsonGet[NextAnswerId]['NextAnswerNo']['A5'];
                response = jsonGet[NextNo]['answer'];
                URL = jsonGet[NextNo]['url'];
                insertDataLeft(response, URL);
                Returnid = jsonGet[NextNo]['id'];
            }
        }

    }
    else {
        console.log('単発')
        console.log('id:'+id)

        if (jsonGet[id]['Keyword'] != '') {
            if (Para.match(jsonGet[id]['Keyword'])) {
                insertDataLeft('こちらでいかがでしょうか',);
                response = jsonGet[id]['answer'];
                URL = jsonGet[id]['url'];
                insertDataLeft(response, URL);
                Returnid = jsonGet[id]['id'];
                console.log('Returnid:'+Returnid)
            }
            else {

            }
            console.log('111111Returnid:'+Returnid)
        if(jsonGet[Returnid]['question']['Q1']==' ')
        {
            NextAnswerId=0;
            console.log('yes')
            console.log('0000000NextAnswerId:'+NextAnswerId)
        }
        }
    }
    return Returnid
}
/*
var jsonGet = [
    {
        id: 0,
        Keyword: '',
        answer: 'すみません。こちらをご参照ください。',
        url: 'https://support.flypeach.com/hc/ja',
        question: {Q1: ' ', Q2: ' ', Q3: ' ', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: ' ', A2: ' ', A3: ' ', A4: ' ', A5: ' '}
    },
    {
        id: 1,
        Keyword: 'オプション',
        answer: '各種オプションサービス（座席指定・手荷物）\nの追加料金について。\n',
        url: 'https://support.flypeach.com/hc/ja/articles/115001302813',
        question: {Q1: ' ', Q2: ' ', Q3: ' ', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: ' ', A2: ' ', A3: ' ', A4: ' ', A5: ' '}
    },
    {
        id: 2,
        Keyword: 'サービス',
        answer: '各種オプションサービス（座席指定・手荷物）\nの追加料金について。\n',
        url: 'https://support.flypeach.com/hc/ja/articles/115001302813',
        question: {Q1: ' ', Q2: ' ', Q3: ' ', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: ' ', A2: ' ', A3: ' ', A4: ' ', A5: ' '}
    },
    {
        id: 3,
        Keyword: '手荷物',
        answer: '手荷物についてどのようなご用件でしょうか。'+'<br>'+'1:値段について'+'<br>'+'2:機内持ち込みについて'+'<br>'+'3:その他',
        url: '',
        question: {Q1: '値段', Q2: '機内', Q3: 'その他', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: '4', A2: '5', A3: '6', A4: ' ', A5: ' '}
    },
    {
        id: 4,
        Keyword: '',
        answer: '各種オプションサービス（座席指定・手荷物）\nの追加料金について。\n',
        url: 'https://support.flypeach.com/hc/ja/articles/115001302813',
        question: {Q1: ' ', Q2: ' ', Q3: ' ', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: ' ', A2: ' ', A3: ' ', A4: ' ', A5: ' '}
    },
    {
        id: 5,
        Keyword: '',
        answer: '機内への手荷物の持ち込みについて。',
        url: 'https://support.flypeach.com/hc/ja/articles/115001301214',
       question: {Q1: ' ', Q2: ' ', Q3: ' ', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: ' ', A2: ' ', A3: ' ', A4: ' ', A5: ' '}
    },
    {
        id: 6,
        Keyword: '',
        answer: '航空券購入後の、受託手荷物を別途追加について。',
        url: 'https://support.flypeach.com/hc/ja/articles/115001302813',
        question: {Q1: ' ', Q2: ' ', Q3: ' ', Q4: ' ', Q5: ' '},
        NextAnswerNo: {A1: ' ', A2: ' ', A3: ' ', A4: ' ', A5: ' '}
    }
]
var str = JSON.stringify(jsonGet);
console.log('jsonGet:'+str)
*/

var requestURL = 'http://127.0.0.1:8000/api/qa/?format=json';
var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
  var superHeroes = request.response;
    var str = JSON.stringify(superHeroes);

  console.log('superHeroes:'+str)
  var  jsonGet=str
    console.log('jsonGet:'+jsonGet)
}
