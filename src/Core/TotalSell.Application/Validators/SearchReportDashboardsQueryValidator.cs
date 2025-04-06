using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class SearchReportDashboardsQueryValidator : AbstractValidator<SearchReportDashboardsQuery>
{
    public SearchReportDashboardsQueryValidator()
    {
        RuleFor(x => x.SearchTerm)
            .MaximumLength(100).WithMessage("عبارت جستجو نمی‌تواند بیشتر از 100 کاراکتر باشد")
            .When(x => x.SearchTerm != null);

        RuleFor(x => x.PageNumber)
            .GreaterThan(0).WithMessage("شماره صفحه باید بزرگتر از صفر باشد");

        RuleFor(x => x.PageSize)
            .GreaterThan(0).WithMessage("اندازه صفحه باید بزرگتر از صفر باشد")
            .LessThanOrEqualTo(100).WithMessage("اندازه صفحه نمی‌تواند بیشتر از 100 باشد");

        RuleFor(x => x.SortBy)
            .MaximumLength(50).WithMessage("فیلد مرتب‌سازی نمی‌تواند بیشتر از 50 کاراکتر باشد")
            .When(x => x.SortBy != null);
    }
} 