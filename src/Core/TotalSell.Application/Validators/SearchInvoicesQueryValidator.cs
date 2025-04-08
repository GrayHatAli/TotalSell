using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class SearchInvoicesQueryValidator : AbstractValidator<SearchInvoicesQuery>
{
    public SearchInvoicesQueryValidator()
    {
        RuleFor(x => x.Number)
            .MaximumLength(50);

        RuleFor(x => x.FromDate)
            .LessThanOrEqualTo(x => x.ToDate)
            .When(x => x.FromDate.HasValue && x.ToDate.HasValue)
            .WithMessage("From date must be less than or equal to to date");

        RuleFor(x => x.ToDate)
            .GreaterThanOrEqualTo(x => x.FromDate)
            .When(x => x.FromDate.HasValue && x.ToDate.HasValue)
            .WithMessage("To date must be greater than or equal to from date");

        RuleFor(x => x.MinTotal)
            .LessThanOrEqualTo(x => x.MaxTotal)
            .When(x => x.MinTotal.HasValue && x.MaxTotal.HasValue)
            .WithMessage("Minimum total must be less than or equal to maximum total");

        RuleFor(x => x.MaxTotal)
            .GreaterThanOrEqualTo(x => x.MinTotal)
            .When(x => x.MinTotal.HasValue && x.MaxTotal.HasValue)
            .WithMessage("Maximum total must be greater than or equal to minimum total");
    }
} 