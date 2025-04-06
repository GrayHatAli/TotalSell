using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateReportDashboardVersionCommandValidator : AbstractValidator<CreateReportDashboardVersionCommand>
{
    public CreateReportDashboardVersionCommandValidator()
    {
        RuleFor(x => x.DashboardId)
            .NotEmpty()
            .WithMessage("شناسه داشبورد الزامی است");

        RuleFor(x => x.Version)
            .NotEmpty()
            .WithMessage("نسخه الزامی است")
            .MaximumLength(50)
            .WithMessage("نسخه نمی‌تواند بیشتر از 50 کاراکتر باشد");

        RuleFor(x => x.Description)
            .MaximumLength(500)
            .WithMessage("توضیحات نمی‌تواند بیشتر از 500 کاراکتر باشد");

        RuleFor(x => x.Layout)
            .MaximumLength(1000)
            .WithMessage("طرح‌بندی نمی‌تواند بیشتر از 1000 کاراکتر باشد");

        RuleFor(x => x.Theme)
            .MaximumLength(100)
            .WithMessage("تم نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Parameters)
            .MaximumLength(1000)
            .WithMessage("پارامترها نمی‌تواند بیشتر از 1000 کاراکتر باشد");

        RuleFor(x => x.Filters)
            .MaximumLength(1000)
            .WithMessage("فیلترها نمی‌تواند بیشتر از 1000 کاراکتر باشد");

        RuleFor(x => x.RefreshInterval)
            .GreaterThan(0)
            .When(x => x.RefreshInterval.HasValue)
            .WithMessage("فاصله زمانی بروزرسانی باید بزرگتر از صفر باشد");
    }
} 