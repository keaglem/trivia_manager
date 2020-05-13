var s, socket,
App = {
    settings: {
        displayArea: $('#display-area'),
        questionButton: $('#question-btn'),
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
            s.answerArea.empty();
            s.questionButton.click();
        });

        this.bindUIActions();
        this.updateDisplay();
    },


    bindUIActions: function() {
        s.questionButton.click(App.handleButtonClick(App.showQuestions));
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


};


(function() {
    App.init();
})();