let jsConfig = {
    'useColors': undefined,
    'editTransactionsUrl': '',
    'editTransactionActonUrl': ''
};

jsConfig.init = function() {
    if (jsConfig.useColors) {
        jsConfig.colorElements();
    }

    jsConfig.editTransactionClickEvent();
    jsConfig.addTransactionClickEvent();
};

jsConfig.colorElements = function() {
    let randomTextColorElements = [
        ...document.querySelectorAll('.value-with-label p:first-of-type'),
        ...document.querySelectorAll('.expense-group-title'),
        ...document.querySelectorAll('th')
    ];
    let randomBackgroundColorElements = [
        ...document.querySelectorAll('.component-title')
    ];

    randomTextColorElements.forEach(element => {
        element.style.color = randomColor({
            'luminosity': 'bright'
        });
    });
    randomBackgroundColorElements.forEach(element => {
        element.style.backgroundColor = randomColor({
            'luminosity': 'bright'
        });
    });
};

// Edit transaction click event
jsConfig.editTransactionClickEvent = function() {
    document.querySelectorAll('.transaction').forEach(function(e) {
        e.addEventListener('click', function(e) {
            let transactionRow = e.target;
            let transactionId = transactionRow.dataset.id;

            if (transactionId === undefined) {
                transactionRow = transactionRow.closest('.transaction');
                transactionId = transactionRow.dataset.id;
            }

            if (!transactionId) {
                return;
            }

            let existingForm = document.querySelector(`.edit-transaction-form[data-id='${transactionId}']`);
            if (!existingForm) {
                let fullEndpoint = `${jsConfig.editTransactionsUrl}/${transactionId}`;
                fetchWrapper(fullEndpoint, 'get', {}, function(data) {
                    jsConfig.addEditTransactionForm(transactionRow, data);
                });
            }
        });
    });
};

// Add transaction click event
jsConfig.addTransactionClickEvent = function() {
    document.querySelector('.add-transaction-btn').addEventListener('click', function(e) {
        let transactionRow = e.target;
        let fullEndpoint = `${jsConfig.editTransactionsUrl}`;
        fetchWrapper(fullEndpoint, 'get', {}, function(data) {
            jsConfig.addEditTransactionForm(transactionRow, data);
        });
    });
};

jsConfig.addEditTransactionForm = function(transactionRow, data) {
    let top = `${transactionRow.offsetTop + transactionRow.offsetHeight}px`;
    let left = `${transactionRow.offsetLeft}px`;
    let wrapperDiv = document.createElement('div');
    wrapperDiv.style = `position: absolute; top: ${top}; left: ${left};`;
    wrapperDiv.innerHTML = data.html;

    // Add click events to control divs
    let controlDivs = wrapperDiv.querySelectorAll('.edit-transaction-action');
    controlDivs.forEach(function(e) {
        e.addEventListener('click', function(e) {
            jsConfig.editTransactionFormAction(e.target);
        });
    });

    document.body.appendChild(wrapperDiv);
};

jsConfig.editTransactionFormAction = function(controlDiv) {
    let action = controlDiv.dataset.action;
    if (action === 'close') {
        // TODO - need to remove .edit-transaction-form's PARENT node
        controlDiv.closest('.edit-transaction-form').remove();
        return;
    }

    let params = {
        'action': action,
        'transactionId': controlDiv.dataset.id
    };
    fetchWrapper(jsConfig.editTransactionActonUrl, 'post', params, function(data) {
        location.reload();
    });
};
