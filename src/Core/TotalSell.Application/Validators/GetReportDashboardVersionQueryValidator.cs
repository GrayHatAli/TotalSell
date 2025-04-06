using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class GetReportDashboardVersionQueryValidator : AbstractValidator<GetReportDashboardVersionQuery>
{
    public GetReportDashboardVersionQueryValidator()
    {
        RuleFor(x => x.VersionId)
            .NotEmpty().WithMessage("شناسه نسخه الزامی است");
    }
} 