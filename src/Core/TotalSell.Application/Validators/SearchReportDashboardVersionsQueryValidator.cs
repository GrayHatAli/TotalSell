using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class SearchReportDashboardVersionsQueryValidator : AbstractValidator<SearchReportDashboardVersionsQuery>
{
    public SearchReportDashboardVersionsQueryValidator()
    {
        RuleFor(x => x.SearchTerm)
            .MaximumLength(100)
            .WithMessage("عبارت جستجو نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Version)
            .MaximumLength(50)
            .WithMessage("نسخه نمی‌تواند بیشتر از 50 کاراکتر باشد");

        RuleFor(x => x.Status)
            .MaximumLength(50)
            .WithMessage("وضعیت نمی‌تواند بیشتر از 50 کاراکتر باشد");

        RuleFor(x => x.PageNumber)
            .GreaterThan(0)
            .WithMessage("شماره صفحه باید بزرگتر از 0 باشد");

        RuleFor(x => x.PageSize)
            .GreaterThan(0)
            .WithMessage("اندازه صفحه باید بزرگتر از 0 باشد")
            .LessThanOrEqualTo(100)
            .WithMessage("اندازه صفحه نمی‌تواند بیشتر از 100 باشد");

        RuleFor(x => x.SortBy)
            .MaximumLength(50)
            .WithMessage("فیلد مرتب‌سازی نمی‌تواند بیشتر از 50 کاراکتر باشد");
    }
} 