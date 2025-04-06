using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class RejectReportDashboardVersionCommandValidator : AbstractValidator<RejectReportDashboardVersionCommand>
{
    public RejectReportDashboardVersionCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty()
            .WithMessage("شناسه نسخه الزامی است");

        RuleFor(x => x.RejectedBy)
            .NotEmpty()
            .WithMessage("نام رد کننده الزامی است")
            .MaximumLength(100)
            .WithMessage("نام رد کننده نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.RejectionReason)
            .NotEmpty()
            .WithMessage("دلیل رد الزامی است")
            .MaximumLength(500)
            .WithMessage("دلیل رد نمی‌تواند بیشتر از 500 کاراکتر باشد");
    }
} 