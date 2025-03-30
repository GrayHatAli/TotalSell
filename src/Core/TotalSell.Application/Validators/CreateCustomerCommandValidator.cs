using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateCustomerCommandValidator : AbstractValidator<CreateCustomerCommand>
{
    public CreateCustomerCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("نام مشتری نمی‌تواند خالی باشد")
            .MaximumLength(100).WithMessage("نام مشتری نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Code)
            .NotEmpty().WithMessage("کد مشتری نمی‌تواند خالی باشد")
            .MaximumLength(20).WithMessage("کد مشتری نمی‌تواند بیشتر از 20 کاراکتر باشد");

        When(x => !string.IsNullOrWhiteSpace(x.NationalCode), () =>
        {
            RuleFor(x => x.NationalCode)
                .Length(10).WithMessage("کد ملی باید 10 رقم باشد")
                .Matches("^[0-9]*$").WithMessage("کد ملی فقط می‌تواند شامل اعداد باشد");
        });

        When(x => !string.IsNullOrWhiteSpace(x.EconomicCode), () =>
        {
            RuleFor(x => x.EconomicCode)
                .Length(12).WithMessage("کد اقتصادی باید 12 رقم باشد")
                .Matches("^[0-9]*$").WithMessage("کد اقتصادی فقط می‌تواند شامل اعداد باشد");
        });

        When(x => !string.IsNullOrWhiteSpace(x.Email), () =>
        {
            RuleFor(x => x.Email)
                .EmailAddress().WithMessage("فرمت ایمیل صحیح نیست");
        });

        When(x => !string.IsNullOrWhiteSpace(x.PhoneNumber), () =>
        {
            RuleFor(x => x.PhoneNumber)
                .Matches("^[0-9]*$").WithMessage("شماره تلفن فقط می‌تواند شامل اعداد باشد")
                .Length(11).WithMessage("شماره تلفن باید 11 رقم باشد");
        });

        When(x => !string.IsNullOrWhiteSpace(x.MobileNumber), () =>
        {
            RuleFor(x => x.MobileNumber)
                .Matches("^[0-9]*$").WithMessage("شماره موبایل فقط می‌تواند شامل اعداد باشد")
                .Length(11).WithMessage("شماره موبایل باید 11 رقم باشد");
        });
    }
} 