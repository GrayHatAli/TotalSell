using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateReportCommandValidator : AbstractValidator<CreateReportCommand>
{
    public CreateReportCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("نام گزارش نمی‌تواند خالی باشد")
            .MaximumLength(100).WithMessage("نام گزارش نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Code)
            .NotEmpty().WithMessage("کد گزارش نمی‌تواند خالی باشد")
            .MaximumLength(20).WithMessage("کد گزارش نمی‌تواند بیشتر از 20 کاراکتر باشد");

        RuleFor(x => x.Type)
            .NotEmpty().WithMessage("نوع گزارش نمی‌تواند خالی باشد")
            .IsInEnum().WithMessage("نوع گزارش معتبر نیست");

        When(x => x.RefreshInterval.HasValue, () =>
        {
            RuleFor(x => x.RefreshInterval)
                .GreaterThan(0).WithMessage("فاصله به‌روزرسانی باید بیشتر از صفر باشد");
        });

        When(x => !string.IsNullOrWhiteSpace(x.Parameters), () =>
        {
            RuleFor(x => x.Parameters)
                .Must(BeValidJson).WithMessage("فرمت پارامترها معتبر نیست");
        });

        When(x => !string.IsNullOrWhiteSpace(x.Filters), () =>
        {
            RuleFor(x => x.Filters)
                .Must(BeValidJson).WithMessage("فرمت فیلترها معتبر نیست");
        });
    }

    private bool BeValidJson(string json)
    {
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