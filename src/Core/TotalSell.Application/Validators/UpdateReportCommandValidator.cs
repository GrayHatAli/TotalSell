using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class UpdateReportCommandValidator : AbstractValidator<UpdateReportCommand>
{
    public UpdateReportCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("شناسه گزارش الزامی است");

        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("نام گزارش الزامی است")
            .MaximumLength(100).WithMessage("نام گزارش نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Code)
            .NotEmpty().WithMessage("کد گزارش الزامی است")
            .MaximumLength(20).WithMessage("کد گزارش نمی‌تواند بیشتر از 20 کاراکتر باشد")
            .Matches("^[a-zA-Z0-9_-]+$").WithMessage("کد گزارش باید شامل حروف انگلیسی، اعداد، خط تیره و زیرخط باشد");

        RuleFor(x => x.Type)
            .NotEmpty().WithMessage("نوع گزارش الزامی است")
            .MaximumLength(50).WithMessage("نوع گزارش نمی‌تواند بیشتر از 50 کاراکتر باشد");

        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("توضیحات نمی‌تواند بیشتر از 500 کاراکتر باشد")
            .When(x => x.Description != null);

        RuleFor(x => x.CategoryId)
            .NotEmpty().WithMessage("دسته‌بندی گزارش الزامی است");

        RuleFor(x => x.Query)
            .NotEmpty().WithMessage("پرس و جوی گزارش الزامی است")
            .When(x => x.Type == "SQL");

        RuleFor(x => x.Parameters)
            .Must(BeValidJson).WithMessage("پارامترها باید در قالب JSON معتبر باشند")
            .When(x => x.Parameters != null);

        RuleFor(x => x.Filters)
            .Must(BeValidJson).WithMessage("فیلترها باید در قالب JSON معتبر باشند")
            .When(x => x.Filters != null);

        RuleFor(x => x.RefreshInterval)
            .GreaterThan(0).WithMessage("فاصله زمانی به‌روزرسانی باید بزرگتر از صفر باشد")
            .When(x => x.RefreshInterval.HasValue);

        RuleFor(x => x.Layout)
            .Must(BeValidJson).WithMessage("طرح‌بندی باید در قالب JSON معتبر باشد")
            .When(x => x.Layout != null);

        RuleFor(x => x.Theme)
            .MaximumLength(50).WithMessage("تم نمی‌تواند بیشتر از 50 کاراکتر باشد")
            .When(x => x.Theme != null);
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