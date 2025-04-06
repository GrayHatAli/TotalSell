using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class GetReportDashboardQueryValidator : AbstractValidator<GetReportDashboardQuery>
{
    public GetReportDashboardQueryValidator()
    {
        RuleFor(x => x.DashboardId)
            .NotEmpty().WithMessage("شناسه داشبورد الزامی است");
    }
} 