function drawRaty(evaluateItem, score, readOnly) {
    var ratyId = '#' + evaluateItem;
    var starId = ratyId + "_star";
    var targetId = ratyId + "_target";
    var target = $(targetId);
    target.html('0.0');
    $(starId).raty({
        half: true,
        halfShow: true,
        precision: true,

        path: '/static/images/raty',
        space: false,
        //hints: ['0.0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0'],
        target: targetId,
        targetKeep: true,
        targetType: 'number',
        mouseover: function (score, evt) {
            if (score === null) {
                target.html('0.0');
            } else if (score === undefined) {
                target.empty();
            } else {
                score = (Math.round(score * 2) / 2).toFixed(1);
                target.html(score);

            }
        },
        click: function (score, evt) {
            $(this).fadeOut(function () {
                $(this).fadeIn();
            });
            score = target.html();
            score = (Math.round(score * 2) / 2).toFixed(1);
            $(starId).children().last().val(score);
            return false;
        },
        round: {down: .25, full: .6, up: .8},
        readOnly: readOnly,
        score: score
    });
}
