from django.shortcuts import render
from .models import DailyAnalysis
from analyzer.services.probability_weights import (
    generate_probability_table,
    lowest_weighted_numbers,
)



def analysis_list(request):
    records = (
        DailyAnalysis.objects
        .select_related('source')
        .order_by('-date', 'day')
    )

    # Prepare values for template display
    for r in records:
        r.open_digits = list(f"{r.open_value:03d}")    # ['7','9','9']
        r.close_digits = list(f"{r.close_value:03d}")  # ['1','5','5']

    return render(
        request,
        'analyzer/list.html',
        {
            'records': records
        }
    )


def probability_table(request):
    table = generate_probability_table()
    return render(
        request,
        "analyzer/probability_table.html",
        {"table": table}
    )


def probability_table_view(request):
    filter_type = request.GET.get("filter")

    if filter_type == "lowest":
        table = lowest_weighted_numbers(5)

    elif filter_type == "below":
        table = filter_by_probability(max_prob=0.9)

    else:
        table = generate_probability_table()

    return render(request, "probability_table.html", {
        "table": table,
        "filter": filter_type
    })