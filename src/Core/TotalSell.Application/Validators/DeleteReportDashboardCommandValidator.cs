using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class DeleteReportDashboardCommandValidator : AbstractValidator<DeleteReportDashboardCommand>
{
    public DeleteReportDashboardCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("شناسه داشبورد الزامی است");
    }
} 