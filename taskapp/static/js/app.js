var s, socket,
App = {
    settings: {
        displayArea: $('#display-area'),
        viewButton: $('#view-btn'),
        simButton: $('#sim-btn'),
        allSimButton: $('#all-sim-btn'),
        submitButton: $('#submit-btn'),
        lastClicked: $('#view-btn'),
        topNavBar: $('#top-nav-bar'),
        connectedStatus: $('#connected-status'),
        jobStatus: $('#job-status')
    },

    init: function() {
        s = this.settings;
        socket = io.connect('http://' + document.domain + ':' + location.port + '/live_connect');
        socket.on('connect', function() {
            s.jobStatus.text('0 remaining jobs');
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

        this.bindUIActions();
        this.updateDisplay();
    },


    bindUIActions: function() {
        s.viewButton.click(App.handleButtonClick(App.showSubmissions));
        s.submitButton.click(App.handleButtonClick(App.showSubmit));
        s.simButton.click(App.handleButtonClick(App.showSimulations));
        s.allSimButton.click(App.handleButtonClick(App.showAllSimulations));
        // TODO: add this functionality back for cluster display
        //s.deviceSelect.change(App.updateDisplay);
    },

    getValidURI: function(base, id) {
        if(typeof(id)==='undefined') 
            return base;
        if (id === null)
            return base;
        return base + '/' + id;
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
    showSubmissionText: function(e) {
        id = $(this).data('subId');
        s.displayArea.load(App.getValidURI('/api/simulations',id))
    },
    showSubmit: function(e) {
        s.displayArea.load('/api/upload')
    },
    showSimulations: function(e) {
        s.displayArea.load('/api/simulations')

    },
    showAllSimulations: function(e) {
        s.displayArea.load('/api/all_simulations')
    },
    showSubmissions: function(e) {
        s.displayArea.load('/api/submissions');
        App.loadNoCache(s.displayArea, '/api/submissions', function (){
            $('tr[data-sub-id]').click(App.showSubmissionText)
        })
    },


};


(function() {
    App.init();
})();