using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class GetInvoiceQueryValidator : AbstractValidator<GetInvoiceQuery>
{
    public GetInvoiceQueryValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty();
    }
} 