        <div class="row">
            <div class="col-md-12">
                <form method="post" action="?page=search" role="form" class="form-floating" name="search">
                    <div class="col-auto">
                        <label for="question">Write your question below:</label>
                        <div class="input-group mb-2">
                            <input type="text" name="question" placeholder="How can I help you?" class="form-control text-monospace"
                                autocomplete="off" required="required" value="">
                            <input type="hidden" name="id" value="">
                            <div class="input-group-append">
                                <button name="btnSearch" class="btn btn-primary" type="submit">Search!</button>
                            </div>
                        </div>
                    </div>
                </form>
                <div class="h-100 invisible bg-dark rounded mx-3" name="output">
                    <div class="row h-100">
                        <span name="result" class="container d-flex align-items-center justify-content-center text-monospace"></span>
                    </div>
                </div>
            </div>
        </div>