var s, socket,
App = {
    settings: {
        displayArea: $('#display-area'),
        questionButton: $('#question-btn'),
        responsesButton: $('#responses-btn'),
        scoreboardButton: $('#scoreboard-btn'),
        answerArea: $('#answer-area'),
        lastClicked: $('#question-btn'),
        topNavBar: $('#top-nav-bar'),
        connectedStatus: $('#connected-status'),
        jobStatus: $('#job-status')
    },

    init: function() {
        s = this.settings;
        socket = io.connect('http://' + document.domain + ':' + location.port + '/live_connect');
        socket.on('connect', function() {
            s.jobStatus.text('Welcome!');
            s.connectedStatus.text('Connected');
            socket.emit('my event', {data: 'I\'m connected!'});
        });
        socket.on('disconnect', function() {
            s.jobStatus.text('');
            s.connectedStatus.text('Not Connected');
        });
        socket.on('active jobs', function(inputData) {
            s.jobStatus.text(inputData.num_jobs + ' remaining jobs');
        });
        socket.on('current question', function(inputData) {
            s.jobStatus.text('Current question: ' + inputData.question_id + '.');
            if (s.lastClicked == s.questionButton[0]) {
                s.answerArea.empty();
                s.questionButton.click();
            }            
        });
        socket.on('question answered', function(inputData) {
            inputData.forEach(function (item, idx) {
                $('#prompt-'+item.prompt_id + ' > tbody')
                    .append($('<tr>').attr('data-prompt-id', item.answer_id)
                        .append($('<td>')
                            .text(item.user_name))
                        .append($('<td>')
                            .text(item.received_answer))
                        .append($('<td>')
                            .text(item.points_received)));
            });
        });

        this.bindUIActions();
        this.updateDisplay();
    },


    bindUIActions: function() {
        s.questionButton.click(App.handleButtonClick(App.showQuestions));
        s.responsesButton.click(App.handleButtonClick(App.showResponses));
        s.scoreboardButton.click(App.handleButtonClick(App.showScoreboard));
    },

    loadNoCache: function(elem, url, success) {
        $.ajax(url, {
            dataType: 'html',
            cache: false,
            success: function(data) {
                elem.html(data);
                success();
            }
        });
    },

    updateDisplay: function() {
        s.lastClicked.click();
    },

    handleButtonClick: function(displayCallback) {
        return function(e) {
            $(this).siblings().removeClass('active');
            $(this).addClass('active');
            s.lastClicked = this;
            return displayCallback();
        }
    },
    showQuestions: function(e) {
        s.displayArea.load('/api/question');
    },
    showResponses: function(e) {
        s.answerArea.empty();
        s.displayArea.load('/api/responses');
    },
    showScoreboard: function(e) {
        s.answerArea.empty();
        s.displayArea.load('/api/scoreboard');
    },

};


(function() {
    App.init();
})();