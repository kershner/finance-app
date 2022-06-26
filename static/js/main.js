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

            // Remove existing forms
            let clickingExistingForm = false;
            document.querySelectorAll(`.edit-transaction-form`).forEach(function(e) {
                clickingExistingForm =  transactionId === e.dataset.id;
                e.remove()
            });

            // Only show the form is user is not clicking on same form that's already open (UX shortcut)
            if (!clickingExistingForm) {
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
        let existingForms = document.querySelectorAll('.edit-transaction-form');
        if (existingForms) {
            for (const form of existingForms) {
                form.remove()
            }
        }

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

    document.body.appendChild(wrapperDiv);
};

jsConfig.editTransactionFormAction = function(controlDiv) {
    let action = controlDiv.dataset.action;
    switch (action) {
        case 'close':
            // TODO - need to remove .edit-transaction-form's PARENT node
            controlDiv.closest('.edit-transaction-form').remove();
            return;
            break;
        case 'add-group':
            // Unhide the add group form, hide transaction group inputs
            jsConfig.toggleAddGroupForm(controlDiv);
            return;
            break;
        case 'delete':
            if (!confirm('Are you sure you\'d like to delete this transaction?')) {
                return;
            }
            break;
    }

    let params = {
        'action': action,
        'transactionId': controlDiv.dataset.id
    };
    fetchWrapper(jsConfig.editTransactionActonUrl, 'post', params, function() {
        location.reload();
    });
};

jsConfig.toggleAddGroupForm = function(controlDiv) {
    let showForm = !hasClass(controlDiv, 'active');
    let addFromWrapper = document.querySelector('.add-group-form-wrapper');
    let groupNameInput = document.querySelector('input[name="group_name"]');

    jsConfig.showHideTransactionTypeSelects(showForm);
    if (showForm) {
        removeClass(addFromWrapper, 'hidden');
        addClass(controlDiv, 'active');
        groupNameInput.required = true;
    }   else {
        addClass(addFromWrapper, 'hidden');
        removeClass(controlDiv, 'active');
        groupNameInput.required = false;
    }
};

jsConfig.showHideTransactionTypeSelects = function(show) {
    let transactionGroupSelect = document.querySelector('select[name="group"]');
    let transactionTypeSelect = document.querySelector('select[name="type"]');
    if (transactionGroupSelect) {
        if (show) {
            addClass(transactionGroupSelect.parentNode, 'hidden');
        } else {
            removeClass(transactionGroupSelect.parentNode, 'hidden');
        }
    }
    if (transactionTypeSelect) {
        if (show) {
            addClass(transactionTypeSelect.parentNode, 'hidden');
        } else {
            removeClass(transactionTypeSelect.parentNode, 'hidden');
        }
    }
};