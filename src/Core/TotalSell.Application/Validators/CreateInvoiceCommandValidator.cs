using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateInvoiceCommandValidator : AbstractValidator<CreateInvoiceCommand>
{
    public CreateInvoiceCommandValidator()
    {
        RuleFor(x => x.Number)
            .NotEmpty()
            .MaximumLength(50);

        RuleFor(x => x.Date)
            .NotEmpty();

        RuleFor(x => x.Description)
            .MaximumLength(500);

        RuleFor(x => x.DueDate)
            .NotEmpty()
            .GreaterThan(x => x.Date)
            .WithMessage("Due date must be after invoice date");

        RuleFor(x => x.Status)
            .IsInEnum();

        RuleFor(x => x.Type)
            .IsInEnum();

        RuleFor(x => x.CustomerId)
            .NotEmpty();

        RuleFor(x => x.ReferenceNumber)
            .MaximumLength(50);

        RuleFor(x => x.PaymentMethod)
            .MaximumLength(50);

        RuleFor(x => x.Items)
            .NotEmpty()
            .WithMessage("Invoice must have at least one item");

        RuleForEach(x => x.Items)
            .SetValidator(new CreateInvoiceItemCommandValidator());
    }
}

public class CreateInvoiceItemCommandValidator : AbstractValidator<CreateInvoiceItemCommand>
{
    public CreateInvoiceItemCommandValidator()
    {
        RuleFor(x => x.ProductId)
            .NotEmpty();

        RuleFor(x => x.Quantity)
            .GreaterThan(0);

        RuleFor(x => x.UnitPrice)
            .GreaterThan(0);

        RuleFor(x => x.DiscountAmount)
            .GreaterThanOrEqualTo(0);

        RuleFor(x => x.TaxAmount)
            .GreaterThanOrEqualTo(0);
    }
} 