using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class GetReportDashboardItemQueryValidator : AbstractValidator<GetReportDashboardItemQuery>
{
    public GetReportDashboardItemQueryValidator()
    {
        RuleFor(x => x.ItemId)
            .NotEmpty().WithMessage("شناسه آیتم الزامی است");
    }
} 