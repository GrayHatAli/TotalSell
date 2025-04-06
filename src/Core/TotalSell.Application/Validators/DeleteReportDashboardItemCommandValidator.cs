using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class DeleteReportDashboardItemCommandValidator : AbstractValidator<DeleteReportDashboardItemCommand>
{
    public DeleteReportDashboardItemCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("شناسه آیتم الزامی است");
    }
} 