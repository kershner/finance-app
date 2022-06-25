let jsConfig = {
    'editTransactionsUrl': '',
    'editTransactionActonUrl': ''
};

jsConfig.init = function() {
    jsConfig.editTransactionClickEvent();
    jsConfig.addTransactionClickEvent();
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
        fetchWrapper(jsConfig.editTransactionsUrl, 'get', {}, function(data) {
            jsConfig.addEditTransactionForm(e.target, data);
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

    // TODO - left off here, want to be able to add new groups from the Edit Transaction Menu
    wrapperDiv.querySelector('select[name="group"]').addEventListener('change', function(e) {
        let select = e.target;
        console.log(select.value);
        console.log(typeof(select.value));
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
    fetchWrapper(jsConfig.editTransactionActonUrl, 'post', params, function() {
        location.reload();
    });
};
