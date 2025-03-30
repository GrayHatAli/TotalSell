using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateInvoiceCommandValidator : AbstractValidator<CreateInvoiceCommand>
{
    public CreateInvoiceCommandValidator()
    {
        RuleFor(x => x.Number)
            .NotEmpty().WithMessage("شماره فاکتور نمی‌تواند خالی باشد")
            .MaximumLength(20).WithMessage("شماره فاکتور نمی‌تواند بیشتر از 20 کاراکتر باشد");

        RuleFor(x => x.Date)
            .NotEmpty().WithMessage("تاریخ فاکتور نمی‌تواند خالی باشد")
            .LessThanOrEqualTo(DateTime.UtcNow).WithMessage("تاریخ فاکتور نمی‌تواند از تاریخ امروز بیشتر باشد");

        When(x => x.DueDate.HasValue, () =>
        {
            RuleFor(x => x.DueDate)
                .GreaterThan(x => x.Date).WithMessage("تاریخ سررسید باید بعد از تاریخ فاکتور باشد");
        });

        RuleFor(x => x.Items)
            .NotEmpty().WithMessage("فاکتور باید حداقل یک آیتم داشته باشد");

        RuleForEach(x => x.Items).SetValidator(new CreateInvoiceItemCommandValidator());
    }
}

public class CreateInvoiceItemCommandValidator : AbstractValidator<CreateInvoiceItemCommand>
{
    public CreateInvoiceItemCommandValidator()
    {
        RuleFor(x => x.ProductId)
            .NotEmpty().WithMessage("شناسه محصول نمی‌تواند خالی باشد");

        RuleFor(x => x.Quantity)
            .GreaterThan(0).WithMessage("تعداد باید بیشتر از صفر باشد");

        RuleFor(x => x.UnitPrice)
            .GreaterThan(0).WithMessage("قیمت واحد باید بیشتر از صفر باشد");

        RuleFor(x => x.DiscountAmount)
            .GreaterThanOrEqualTo(0).WithMessage("مبلغ تخفیف نمی‌تواند منفی باشد")
            .LessThanOrEqualTo(x => x.UnitPrice * x.Quantity)
            .WithMessage("مبلغ تخفیف نمی‌تواند از مبلغ کل بیشتر باشد");

        RuleFor(x => x.TaxAmount)
            .GreaterThanOrEqualTo(0).WithMessage("مبلغ مالیات نمی‌تواند منفی باشد");
    }
} 