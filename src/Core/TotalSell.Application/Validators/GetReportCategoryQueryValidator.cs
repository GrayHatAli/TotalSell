using FluentValidation;
using TotalSell.Application.Queries;

namespace TotalSell.Application.Validators;

public class GetReportCategoryQueryValidator : AbstractValidator<GetReportCategoryQuery>
{
    public GetReportCategoryQueryValidator()
    {
        RuleFor(x => x.CategoryId)
            .NotEmpty().WithMessage("شناسه دسته‌بندی الزامی است");
    }
} 