using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class ApproveReportDashboardVersionCommandValidator : AbstractValidator<ApproveReportDashboardVersionCommand>
{
    public ApproveReportDashboardVersionCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty()
            .WithMessage("شناسه نسخه الزامی است");

        RuleFor(x => x.ApprovedBy)
            .NotEmpty()
            .WithMessage("نام تایید کننده الزامی است")
            .MaximumLength(100)
            .WithMessage("نام تایید کننده نمی‌تواند بیشتر از 100 کاراکتر باشد");
    }
} 