using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class DeleteReportDashboardVersionCommandValidator : AbstractValidator<DeleteReportDashboardVersionCommand>
{
    public DeleteReportDashboardVersionCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty()
            .WithMessage("شناسه نسخه الزامی است");
    }
} 