using Microsoft.AspNetCore.Mvc;
using MediatR;
using TotalSell.Application.Commands;
using TotalSell.Application.Queries;
using TotalSell.Application.DTOs;

namespace TotalSell.API.Controllers;

public class ReportsController : BaseController
{
    public ReportsController(IMediator mediator) : base(mediator)
    {
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ReportDto>>> GetReports()
    {
        var query = new SearchReportsQuery();
        var result = await _mediator.Send(query);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ReportDto>> GetReport(Guid id)
    {
        var query = new GetReportQuery { ReportId = id };
        var result = await _mediator.Send(query);
        if (result == null)
            return NotFound();
        return Ok(result);
    }

    [HttpPost]
    public async Task<ActionResult<Guid>> CreateReport(CreateReportCommand command)
    {
        var result = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetReport), new { id = result }, result);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult> UpdateReport(Guid id, UpdateReportCommand command)
    {
        if (id != command.Id)
            return BadRequest();
        
        await _mediator.Send(command);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> DeleteReport(Guid id)
    {
        var command = new DeleteReportCommand { Id = id };
        await _mediator.Send(command);
        return NoContent();
    }
} 