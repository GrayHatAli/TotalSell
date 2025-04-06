using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateReportDashboardVersionCommandValidator : AbstractValidator<CreateReportDashboardVersionCommand>
{
    public CreateReportDashboardVersionCommandValidator()
    {
        RuleFor(x => x.DashboardId)
            .NotEmpty().WithMessage("شناسه داشبورد الزامی است");

        RuleFor(x => x.Version)
            .NotEmpty().WithMessage("نسخه الزامی است")
            .MaximumLength(20).WithMessage("نسخه نمی‌تواند بیشتر از 20 کاراکتر باشد")
            .Matches("^[0-9]+\\.[0-9]+\\.[0-9]+$").WithMessage("نسخه باید در قالب x.y.z باشد");

        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("توضیحات نمی‌تواند بیشتر از 500 کاراکتر باشد")
            .When(x => x.Description != null);

        RuleFor(x => x.Layout)
            .Must(BeValidJson).WithMessage("طرح‌بندی باید در قالب JSON معتبر باشد")
            .When(x => x.Layout != null);

        RuleFor(x => x.Theme)
            .MaximumLength(50).WithMessage("تم نمی‌تواند بیشتر از 50 کاراکتر باشد")
            .When(x => x.Theme != null);

        RuleFor(x => x.Parameters)
            .Must(BeValidJson).WithMessage("پارامترها باید در قالب JSON معتبر باشند")
            .When(x => x.Parameters != null);

        RuleFor(x => x.Filters)
            .Must(BeValidJson).WithMessage("فیلترها باید در قالب JSON معتبر باشند")
            .When(x => x.Filters != null);

        RuleFor(x => x.RefreshInterval)
            .GreaterThan(0).WithMessage("فاصله زمانی به‌روزرسانی باید بزرگتر از صفر باشد")
            .When(x => x.RefreshInterval.HasValue);
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