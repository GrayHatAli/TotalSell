using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateReportDashboardItemCommandValidator : AbstractValidator<CreateReportDashboardItemCommand>
{
    public CreateReportDashboardItemCommandValidator()
    {
        RuleFor(x => x.DashboardId)
            .NotEmpty().WithMessage("شناسه داشبورد الزامی است");

        RuleFor(x => x.Title)
            .NotEmpty().WithMessage("عنوان آیتم الزامی است")
            .MaximumLength(100).WithMessage("عنوان آیتم نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Type)
            .NotEmpty().WithMessage("نوع آیتم الزامی است")
            .MaximumLength(50).WithMessage("نوع آیتم نمی‌تواند بیشتر از 50 کاراکتر باشد");

        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("توضیحات نمی‌تواند بیشتر از 500 کاراکتر باشد")
            .When(x => x.Description != null);

        RuleFor(x => x.Query)
            .NotEmpty().WithMessage("پرس و جوی آیتم الزامی است")
            .When(x => x.Type == "SQL");

        RuleFor(x => x.Parameters)
            .Must(BeValidJson).WithMessage("پارامترها باید در قالب JSON معتبر باشند")
            .When(x => x.Parameters != null);

        RuleFor(x => x.Filters)
            .Must(BeValidJson).WithMessage("فیلترها باید در قالب JSON معتبر باشند")
            .When(x => x.Filters != null);

        RuleFor(x => x.Layout)
            .Must(BeValidJson).WithMessage("طرح‌بندی باید در قالب JSON معتبر باشد")
            .When(x => x.Layout != null);

        RuleFor(x => x.Theme)
            .MaximumLength(50).WithMessage("تم نمی‌تواند بیشتر از 50 کاراکتر باشد")
            .When(x => x.Theme != null);

        RuleFor(x => x.RefreshInterval)
            .GreaterThan(0).WithMessage("فاصله زمانی به‌روزرسانی باید بزرگتر از صفر باشد");

        RuleFor(x => x.Order)
            .GreaterThanOrEqualTo(0).WithMessage("ترتیب باید بزرگتر یا مساوی صفر باشد");
    }

    private static bool BeValidJson(string? json)
    {
        if (string.IsNullOrEmpty(json)) return true;
        try
        {
            System.Text.Json.JsonDocument.Parse(json);
            return true;
        }
        catch
        {
            return false;
        }
    }
} 