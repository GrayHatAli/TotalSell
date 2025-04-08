using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class DeleteInvoiceCommandValidator : AbstractValidator<DeleteInvoiceCommand>
{
    public DeleteInvoiceCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty();
    }
} 