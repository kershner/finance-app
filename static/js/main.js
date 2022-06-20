let jsConfig = {

};

jsConfig.init = function() {
    jsConfig.expandCollapseExpenses();
    jsConfig.addExpenseClickEvent();
};

// Expand/Collapse for the Expenses list
jsConfig.expandCollapseExpenses = function() {
    let expensesToggle = document.querySelectorAll('.expenses-toggle')[0];
    let expensesList = document.querySelectorAll('.expenses-list')[0];

    expensesToggle.addEventListener('click', function(e) {
        if (hasClass(expensesList, 'hidden')) {
            removeClass(expensesList, 'hidden');
            expensesToggle.innerHTML = 'Collapse';
        } else {
            addClass(expensesList, 'hidden');
            expensesToggle.innerHTML = 'Expand';
        }
    });
};

jsConfig.addExpenseClickEvent = function() {
    document.querySelectorAll('.expense').forEach(function(e) {
        e.addEventListener('click', function(e) {
            jsConfig.expenseClickEvent(e.target);
        });
    });
};

jsConfig.expenseClickEvent = function(expense) {
    console.log(expense);
};

jsConfig.init();
